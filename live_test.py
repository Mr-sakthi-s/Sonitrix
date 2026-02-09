import serial
import numpy as np
import joblib
import time

model = joblib.load("ultrasonic_model.pkl")
ser = serial.Serial("COM16", 9600)
WINDOW_SIZE = 20
buffer = []

print("Live Detection Active...")

while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()
    try:
        # Assuming Arduino sends: "time,distance"
        val = float(line.split(',')[1]) if ',' in line else float(line)
        buffer.append(val)
        
        if len(buffer) > WINDOW_SIZE:
            buffer.pop(0)
            
            # Prepare features
            window = np.array(buffer)
            valid = window[window != -1]
            
            if len(valid) > 10:
                mean = np.mean(valid)
                std = np.std(valid)
                rng = np.max(valid) - np.min(valid)
                jit = np.mean(np.abs(np.diff(valid)))
                stab = len(valid) / WINDOW_SIZE
                
                features = np.array([[mean, std, rng, jit, stab]])
                
                pred = model.predict(features)[0]
                prob = model.predict_proba(features)[0]
                
                label = "HARD (Rigid)" if pred == 0 else "SOFT (Absorptive)"
                print(f"Result: {label} | Confidence: {max(prob):.2%}", end='\r')

    except Exception as e:
        continue