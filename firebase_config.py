import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key file
cred = credentials.Certificate("firebase_key.json")

# Your Firebase Realtime Database URL
firebase_url = "https://adaptive-study-default-rtdb.firebaseio.com/"

# Initialize the app
firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_url
})

print("✅ Firebase connected successfully!")
