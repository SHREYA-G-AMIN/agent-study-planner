import firebase_admin
from firebase_admin import credentials, db
import os

def initialize_firebase():
    """Initialize Firebase app - call this once at startup"""
    try:
        # Check if already initialized
        firebase_admin.get_app()
        print("✅ Firebase already initialized")
        return True
    except ValueError:
        pass  # Not initialized yet
    
    # FIX: Remove trailing space in URL!
    firebase_url = "https://adaptivestudyplanner-default-rtdb.asia-southeast1.firebasedatabase.app"
    
    try:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': firebase_url
        })
        print("✅ Firebase connected successfully!")
        return True
    except Exception as e:
        print(f"❌ Firebase init failed: {e}")
        return False
