import time
from datetime import datetime, timezone
from pathlib import Path
from arduino_iot_cloud import ArduinoCloudClient


DEVICE_ID  = "4eba5b6b-d6f4-4d8b-a168-661690be2aa9"
SECRET_KEY = "Fb3VV?Nb79rYwGkb@kHHEZkV#"


VAR_X = "py_x"   # was accelerometer_x
VAR_Y = "py_y"   # was accelerometer_y
VAR_Z = "py_z"   # was accelerometer_z


FILE_X = Path("accel_x.csv")
FILE_Y = Path("accel_y.csv")
FILE_Z = Path("accel_z.csv")

def _ensure_header(p: Path):
    if not p.exists():
        p.write_text("timestamp_iso,value\n", encoding="utf-8")

for p in (FILE_X, FILE_Y, FILE_Z):
    _ensure_header(p)

def _append_csv(path: Path, value):
    ts = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{ts},{value}\n")

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

print("=== iphone accelerometer updates (py_x, py_y, py_z) ===")
print("Writing to accel_x.csv / accel_y.csv / accel_z.csv ... Ctrl+C to stop.\n")

last = {VAR_X: None, VAR_Y: None, VAR_Z: None}
last_write_time = {VAR_X: 0.0, VAR_Y: 0.0, VAR_Z: 0.0}
HOLD_SECONDS = 2.0
SLEEP_SEC = 0.10

try:
    while True:
        client.update()

        now = time.time()
        vx = client.get(VAR_X)
        vy = client.get(VAR_Y)
        vz = client.get(VAR_Z)

        if vx is not None and (vx != last[VAR_X] or now - last_write_time[VAR_X] >= HOLD_SECONDS):
            _append_csv(FILE_X, vx)
            last[VAR_X] = vx
            last_write_time[VAR_X] = now

        if vy is not None and (vy != last[VAR_Y] or now - last_write_time[VAR_Y] >= HOLD_SECONDS):
            _append_csv(FILE_Y, vy)
            last[VAR_Y] = vy
            last_write_time[VAR_Y] = now

        if vz is not None and (vz != last[VAR_Z] or now - last_write_time[VAR_Z] >= HOLD_SECONDS):
            _append_csv(FILE_Z, vz)
            last[VAR_Z] = vz
            last_write_time[VAR_Z] = now

        time.sleep(SLEEP_SEC)

except KeyboardInterrupt:
    print("\nStopped. Files saved:")
    print(f" - {FILE_X.resolve()}")
    print(f" - {FILE_Y.resolve()}")
    print(f" - {FILE_Z.resolve()}")