import serial           # serial communcation
from datetime import datetime, timezone #shows timesamp and date
import time

import firebase_admin #coonects python to firebase
from firebase_admin import credentials, db #bypasses authentication

#the keypath and url of firebase
KEY_PATH = "serviceAccountKey.json" 
DB_URL = "https://sit225-project-906a4-default-rtdb.asia-southeast1.firebasedatabase.app/"

#avoids double intinlization
if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})

# the database references
READINGS_REF = db.reference("/sensors/Gyroscope/readings")
LATEST_REF   = db.reference("/sensors/Gyroscope/latest")

#our port and baud rate for serial port
PORT = "/dev/cu.usbmodem11101"
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=5)
#console texts
print("=== Gyroscope → Firebase Uploader ===")
print(f"Serial: {PORT} @ {BAUD}")
print(f"Firebase DB: {DB_URL}")
print("Press Ctrl+C to stop.\n")

#main reads to parse and uploads loop
try:
    # brief pause 
    time.sleep(0.5)
    ser.reset_input_buffer() #deletes left over buffer

    while True:
        raw = ser.readline()
        line = raw.decode("utf-8", errors="ignore").strip()

        # Skips these lines: blanks / errors / headers
        if not line or line == "ERROR" or line.lower().startswith("timestamp") or "Started" in line:
            continue

        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            # ignores unexpected format
            continue

        try: #convers the values to floats
            gx = float(parts[0])
            gy = float(parts[1])
            gz = float(parts[2])
        except ValueError:
            # ignores the non-numeric row
            continue
            #creates the timestamp
        ts_iso = datetime.now(timezone.utc).isoformat()
        #datas dictonary to firebase
        data = {
            "timestamp_iso": ts_iso,
            "gx_dps": gx,
            "gy_dps": gy,
            "gz_dps": gz
        }

        #upload the newsest data to the database
        LATEST_REF.set(data)

       #saves the data to the database
        READINGS_REF.push(data)
    #shows the confimation text on terminal
        print(f"[UPLOADED] {ts_iso}  gx={gx:.3f}  gy={gy:.3f}  gz={gz:.3f}")

#lets me cloes by ctrl + c
except KeyboardInterrupt:
    print("\nStopped by user.")
# closes the port before exiting
finally:
    ser.close()
    print("Serial port closed.")