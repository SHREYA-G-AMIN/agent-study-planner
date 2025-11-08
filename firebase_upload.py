from firebase_admin import db
import json
import time

def upload_to_firebase(student_id, data):
    """Upload student data to Firebase Realtime Database"""
    try:
        # Reference: /students/{student_id}
        ref = db.reference(f'/students/{student_id}')
        ref.set(data)
        print(f"☁️  Uploaded data for student: {student_id}")
        return True
    except Exception as e:
        print(f"❌ Firebase upload failed: {e}")
        return False

def download_from_firebase(student_id):
    """Download student data from Firebase"""
    try:
        ref = db.reference(f'/students/{student_id}')
        data = ref.get()
        if data:
            print(f"☁️  Downloaded data for student: {student_id}")
        else:
            print(f"ℹ️  No existing data found for {student_id}")
        return data
    except Exception as e:
        print(f"❌ Firebase download failed: {e}")
        return None

def delete_from_firebase(student_id):
    """Delete student data from Firebase"""
    try:
        ref = db.reference(f'/students/{student_id}')
        ref.delete()
        print(f"🗑️  Deleted data for student: {student_id}")
        return True
    except Exception as e:
        print(f"❌ Firebase delete failed: {e}")
        return False

def get_all_students():
    """Get list of all students (for admin features)"""
    try:
        ref = db.reference('/students')
        all_data = ref.get()
        return list(all_data.keys()) if all_data else []
    except Exception as e:
        print(f"❌ Failed to fetch student list: {e}")
        return []
