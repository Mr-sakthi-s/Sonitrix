import serial
import time
import numpy as np
import joblib

PORT = "COM16"
BAUD = 9600
WINDOW = 20

model = joblib.load("hard_soft_model.pkl")
ser = serial.Serial(PORT, BAUD)
time.sleep(2)

buffer = []

print("\nLive Classification Started...\n")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if "," not in line:
            continue

        parts = line.split(",")
        try:
            d = float(parts[1])
        except:
            continue

        if d <= 0:
            buffer.append(np.nan)
        else:
            buffer.append(d)

        if len(buffer) >= WINDOW:
            window = np.array(buffer[-WINDOW:])
            valid = window[~np.isnan(window)]

            if len(valid) < 5:
                continue

            mean = np.mean(valid)
            std = np.std(valid)
            rng = np.max(valid) - np.min(valid)
            jitter = np.mean(np.abs(np.diff(valid)))
            loss_rate = np.isnan(window).sum() / WINDOW

            X = np.array([[mean, std, rng, jitter, loss_rate]])

            pred = model.predict(X)[0]
            prob = model.predict_proba(X)[0][pred]

            if prob < 0.65:
                print("UNCERTAIN | Monitoring")
            elif pred == 0:
                print(f"HARD-LIKE OBJECT | Confidence: {prob:.2f}")
            else:
                print(f"SOFT-LIKE OBJECT | Confidence: {prob:.2f}")

except KeyboardInterrupt:
    print("\nStopped")

ser.close()
