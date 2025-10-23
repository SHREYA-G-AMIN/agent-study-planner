# firebase_upload.py

import firebase_admin
from firebase_admin import credentials, db
import json
from export_json import output_data  # Import your combined JSON

# Step 1: Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://YOUR_PROJECT_ID.firebaseio.com/'  # replace with your DB URL
})

# Step 2: Create a reference for the student
student_ref = db.reference(f"students/{output_data['student_id']}")

# Step 3: Upload data
student_ref.set(output_data)

print("Data uploaded to Firebase successfully!")
