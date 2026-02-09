import serial
import csv
import time

PORT = "COM16"
BAUD = 9600

LABEL = 1  # 0 = Hard, 1 = Soft

ser = serial.Serial(PORT, BAUD)
time.sleep(2)

filename = f"hard_soft_label_{LABEL}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time_ms", "distance_cm", "label"])

    print("Collecting data... Press CTRL+C to stop")

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()

            if "," not in line:
                continue

            try:
                t, d = line.split(",")
                d = float(d)
                writer.writerow([t, d, LABEL])
                print(t, d, LABEL)
            except:
                pass

    except KeyboardInterrupt:
        print("\nStopped")

ser.close()
