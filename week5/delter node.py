import firebase_admin
from firebase_admin import credentials, db

KEY_PATH = "serviceAccountKey.json" 
DB_URL = "https://sit225-project-906a4-default-rtdb.asia-southeast1.firebasedatabase.app/"

if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})

ref = db.reference("/sensors/Gyroscope/readings")
ref.delete()  # 🚨 Irreversible: removes everything under .../readings

print("Deleted /sensors/Gyroscope/readings")