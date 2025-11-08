# test_firebase_download.py
from json_manager import StudentDataManager
import os

# 1. Delete local JSON if it exists
if os.path.exists("student_study_data.json"):
    os.remove("student_study_data.json")
    print("🗑️  Deleted local JSON")

# 2. Create manager with Firebase ONLY (not local)
manager = StudentDataManager(use_firebase=True, student_id="test_sher")

# 3. Load from Firebase - this should find cloud data
data = manager.load_student_data()

# 4. Check if we got real data or default
if data.get("student_name") == "Student" and len(data.get("study_plan", [])) == 0:
    print("⚠️  No data found in Firebase - got defaults")
else:
    print(f"📥 Successfully loaded from Firebase: {data['student_name']}")
    print(f"📚 Topics: {len(data.get('study_plan', []))}")

# 5. Verify local file was created
if os.path.exists("student_study_data.json"):
    print("✅ Local file recreated from Firebase")
else:
    print("❌ Local file not created")