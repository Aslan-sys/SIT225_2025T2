
import time
from datetime import datetime, timezone
from pathlib import Path
from arduino_iot_cloud import ArduinoCloudClient


DEVICE_ID  = "4eba5b6b-d6f4-4d8b-a168-661690be2aa9"
SECRET_KEY = "Fb3VV?Nb79rYwGkb@kHHEZkV#"


VAR_X = "py_x"
VAR_Y = "py_y"
VAR_Z = "py_z"

OUT_PATH = Path("accelerometer_xyz.csv")
VERBOSE  = True           
HOLD_SECONDS = 1.0        
POLL_INTERVAL = 0.10      

if not OUT_PATH.exists():
    OUT_PATH.write_text("timestamp_iso,x,y,z\n", encoding="utf-8")

def write_row(x, y, z):
    ts = datetime.now(timezone.utc).isoformat()
    with OUT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts},{x},{y},{z}\n")
    if VERBOSE:
        print(f"Recorded row: {ts},{x},{y},{z}")

EPS = 1e-6

def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v

def _changed(a, b):
    
    if a is None or b is None:
        return a is not b
    try:
        return abs(float(a) - float(b)) > EPS
    except Exception:
        return a != b

client = ArduinoCloudClient(
    device_id=DEVICE_ID,
    username=DEVICE_ID,
    password=SECRET_KEY,
    sync_mode=True
)

client.register(VAR_X, value=None)
client.register(VAR_Y, value=None)
client.register(VAR_Z, value=None)

client.start()


print(f"Variables: {VAR_X}, {VAR_Y}, {VAR_Z} | Ctrl+C to stop.\n")

latest = {VAR_X: None, VAR_Y: None, VAR_Z: None}
last_written = {VAR_X: None, VAR_Y: None, VAR_Z: None}
last_row_time = 0.0

try:
    while True:
        client.update()

        vx = client.get(VAR_X)
        vy = client.get(VAR_Y)
        vz = client.get(VAR_Z)

        vx = _to_float(vx)
        vy = _to_float(vy)
        vz = _to_float(vz)

        if vx is not None:
            latest[VAR_X] = vx
        if vy is not None:
            latest[VAR_Y] = vy
        if vz is not None:
            latest[VAR_Z] = vz

        have_all = all(latest[v] is not None for v in (VAR_X, VAR_Y, VAR_Z))

        now = time.time()
        changed = (
            _changed(latest[VAR_X], last_written[VAR_X]) or
            _changed(latest[VAR_Y], last_written[VAR_Y]) or
            _changed(latest[VAR_Z], last_written[VAR_Z])
        )
        due_by_hold = HOLD_SECONDS > 0 and (now - last_row_time >= HOLD_SECONDS)

        if have_all and (changed or due_by_hold):
            write_row(latest[VAR_X], latest[VAR_Y], latest[VAR_Z])
            last_written = latest.copy()
            last_row_time = now

        if VERBOSE and have_all:
            print(f"latest → x:{latest[VAR_X]}  y:{latest[VAR_Y]}  z:{latest[VAR_Z]}")

        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nStopped. File saved at:", OUT_PATH.resolve())