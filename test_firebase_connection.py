# test_firebase_connection.py
import firebase_admin
from firebase_admin import credentials, db
import os

try:
    # Initialize
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://adaptivestudyplanner-default-rtdb.asia-southeast1.firebasedatabase.app"
    })
    print("✅ Firebase initialized")
    
    # Try to write
    ref = db.reference('/test')
    ref.set({"message": "Hello Firebase!"})
    print("✅ Write successful")
    
    # Try to read
    data = ref.get()
    print(f"✅ Read successful: {data}")
    
except Exception as e:
    print(f"❌ Error: {e}")