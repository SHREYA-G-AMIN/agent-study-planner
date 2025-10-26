import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://agentstudyplanner-default-rtdb.firebaseio.com/'
})

ref = db.reference("/test_data")
ref.push({
    "message": "Firebase connection successful!",
    "status": "working"
})


print("✅ Firebase test upload successful!")

