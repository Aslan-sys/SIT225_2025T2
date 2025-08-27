
import csv #data into csv
from datetime import datetime #timetsmps and date
import firebase_admin #firebase credentials
from firebase_admin import credentials, db #firebase authentication

KEY_PATH = "serviceAccountKey.json"
DB_URL   = "https://sit225-project-906a4-default-rtdb.asia-southeast1.firebasedatabase.app/"
#avoiuds double intizations
if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})
#refeers to gyroscope readings in firebase
READINGS_REF = db.reference("/sensors/Gyroscope/readings")
#terminal texts
print("=== Firebase → CSV (Gyroscope) ===")
print("Downloading from:", DB_URL)
#gets the data from the wanted node 
snap = READINGS_REF.get()  
#hanldes if the data set is empty and gets out of program
if not snap:
    print("No data found at /sensors/Gyroscope/readings")
    raise SystemExit(0)

#formarts to rows
rows = []
for key, item in snap.items(): #loops through each child node
    
    ts = item.get("timestamp_iso", "")
    gx = item.get("gx_dps", None)
    gy = item.get("gy_dps", None)
    gz = item.get("gz_dps", None)
    rows.append({
        "key": key, #unique key
        "timestamp_iso": ts, #time stamp
        "gx_dps": gx, #x,y,z values
        "gy_dps": gy,
        "gz_dps": gz
    })

#timestamp parsing
def _parse_iso(ts):
    try:
        
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None
#sorts the rows by timestamp
rows.sort(key=lambda r: (_parse_iso(r["timestamp_iso"]) or datetime.min, r["key"]))

#puts the data into csv
out_path = "gyro_data_from_database.csv"
with open(out_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp_iso", "gx_dps", "gy_dps", "gz_dps"])
    for r in rows:
        w.writerow([r["timestamp_iso"], r["gx_dps"], r["gy_dps"], r["gz_dps"]])
#confirms output
print(f"Done. Wrote {len(rows)} rows → {out_path}")