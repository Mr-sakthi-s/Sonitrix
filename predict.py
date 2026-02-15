import serial
import time
import numpy as np
import joblib
import pandas as pd

# ================= USER SETTINGS =================

PORT = "COM16"
BAUD = 9600

MAX_DISTANCE = 100        # cm (change anytime)
WINDOW = 20
PRINT_INTERVAL = 1.0      # seconds

HARD_THRESHOLD = 0.60

MODEL_PATH = "hard_soft_model.pkl"

# =================================================

print("\nLoading model...")
model = joblib.load(MODEL_PATH)

print("Connecting to Arduino...")
ser = serial.Serial(PORT, BAUD)
time.sleep(2)
print("Connected.\n")

buffer = []
last_print_time = time.time()

print("===== LIVE OBJECT CLASSIFICATION STARTED =====\n")

try:
    while True:

        line = ser.readline().decode(errors="ignore").strip()

        if "," not in line:
            continue

        parts = line.split(",")

        try:
            distance = float(parts[1])
        except:
            continue

        # -------- HARD NO OBJECT FILTER ----------
        if distance <= 0 or distance > MAX_DISTANCE:
            distance = -1
        # -----------------------------------------

        buffer.append(distance)

        if len(buffer) > WINDOW:
            buffer.pop(0)

        # ---------- Print every 1 second ----------
        if time.time() - last_print_time < PRINT_INTERVAL:
            continue
        last_print_time = time.time()
        # -----------------------------------------

        window = np.array(buffer)

        # ============== NO OBJECT =================
        if np.all(window == -1):
            print("Object Type : NO OBJECT")
            print("Confidence  : ---")
            print("-----------------------------------")
            continue
        # =========================================

        valid = window[window != -1]

        if len(valid) < 5:
            print("Object Type : NO OBJECT")
            print("Confidence  : ---")
            print("-----------------------------------")
            continue

        # ========== FEATURE EXTRACTION ==========
        mean = np.mean(valid)
        std = np.std(valid)
        rng = np.max(valid) - np.min(valid)
        jitter = np.mean(np.abs(np.diff(valid)))
        loss_rate = np.sum(window == -1) / WINDOW
        # ========================================

        X = pd.DataFrame(
            [[mean, std, rng, jitter, loss_rate]],
            columns=model.feature_names_in_
        )

        probs = model.predict_proba(X)[0]

        hard_prob = probs[0]
        soft_prob = probs[1]

        # ========= CORRECT THRESHOLD LOGIC =======
        if hard_prob >= HARD_THRESHOLD:
            print("Object Type : HARD-LIKE OBJECT")
            print(f"Confidence  : {hard_prob:.2f}")
        else:
            print("Object Type : SOFT-LIKE OBJECT")
            print(f"Confidence  : {soft_prob:.2f}")
        # =========================================

        print("-----------------------------------")

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    ser.close()
    print("Serial port closed")
