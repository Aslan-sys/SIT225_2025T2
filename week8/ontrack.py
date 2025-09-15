# sanity_read.py
import time
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID  = "4eba5b6b-d6f4-4d8b-a168-661690be2aa9"
SECRET_KEY = "Fb3VV?Nb79rYwGkb@kHHEZkV#"
VAR_X, VAR_Y, VAR_Z = "py_x", "py_y", "py_z"

client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)
client.register(VAR_X, value=None)
client.register(VAR_Y, value=None)
client.register(VAR_Z, value=None)
client.start()

print("Reading py_x, py_y, py_z for ~10s… move the phone and watch values:")
t0 = time.time()
while time.time() - t0 < 10:
    client.update()
    vx = client.get(VAR_X); vy = client.get(VAR_Y); vz = client.get(VAR_Z)
    print("x:", vx, " y:", vy, " z:", vz)
    time.sleep(0.1)