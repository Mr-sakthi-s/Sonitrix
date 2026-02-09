import serial
import csv
import time
import os
import numpy as np

PORT = "COM16" 
BAUD = 115200
WINDOW_SIZE = 20

def calculate_features(window, label):
    valid = [d for d in window if d > 0]
    if len(valid) < 5: return None
    return [
        np.mean(valid),
        np.std(valid),
        np.max(valid) - np.min(valid),
        np.mean(np.abs(np.diff(valid))),
        window.count(-1.0) / len(window),
        label
    ]

label = int(input("Enter label (0: HARD, 1: SOFT): "))
filename = f"rich_features_label_{label}.csv"

try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1) # Short timeout to keep loop responsive
    time.sleep(2)
except Exception as e:
    print(f"Error opening port: {e}")
    exit()

file_exists = os.path.isfile(filename)

with open(filename, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["mean", "std", "range", "jitter", "loss_rate", "label"])

    while True:
        cmd = input(f"\n--- [Ready for Label {label}] ---\nPress [Enter] to start 10-second capture, [q] to quit: ")
        if cmd.lower() == 'q': break
        
        raw_buffer = []
        samples_this_burst = 0
        start_time = time.time()
        last_status_time = time.time()
        
        print("COLLECTING... Move object slightly...")

        # Collect for a fixed duration (10 seconds) instead of a count
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if "," in line:
                    try:
                        dist = float(line.split(",")[1])
                        raw_buffer.append(dist)
                        
                        if len(raw_buffer) >= WINDOW_SIZE:
                            features = calculate_features(raw_buffer, label)
                            if features:
                                writer.writerow(features)
                                samples_this_burst += 1
                            raw_buffer.pop(0) 
                    except (ValueError, IndexError):
                        continue

            # Every 1 second, print progress to the terminal
            if time.time() - last_status_time >= 1.0:
                print(f"Time left: {int(10 - (time.time() - start_time))}s | Features saved: {samples_this_burst}")
                last_status_time = time.time()

        f.flush() # Force write data to the CSV file
        print(f"\nSUCCESS: Burst complete. Total features in this session: {samples_this_burst}")

ser.close()