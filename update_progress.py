import json
import firebase_admin
from firebase_admin import credentials, db

# -------------------------------
# 1️⃣ Initialize Firebase
# -------------------------------
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://agentstudyplanner-default-rtdb.firebaseio.com/'
    })

# -------------------------------
# 2️⃣ Load Local JSON Data
# -------------------------------
with open("student_study_data.json", "r") as file:
    local_data = json.load(file)

# -------------------------------
# 3️⃣ Reference to Firebase
# -------------------------------
ref = db.reference("/student_progress")

# -------------------------------
# 4️⃣ Fetch Existing Data from Firebase
# -------------------------------
firebase_data = ref.get()

# -------------------------------
# 5️⃣ Compare and Update Only Changed Fields
# -------------------------------
def sync_data(local, remote, path="/"):
    if remote is None:
        ref.child(path.strip("/")).set(local)
        print(f"🆕 Created new entry: {path}")
        return

    for key, value in local.items():
        new_path = f"{path}/{key}" if path != "/" else key

        if isinstance(value, dict):
            remote_value = remote.get(key) if remote else None
            sync_data(value, remote_value, new_path)
        else:
            if key not in remote or remote[key] != value:
                ref.child(new_path.strip("/")).set(value)
                print(f"🔄 Updated: {new_path} → {value}")

# Perform sync
sync_data(local_data, firebase_data)

# -------------------------------
# 6️⃣ Print Upload Summary
# -------------------------------
print("\n✅ Firebase Sync Complete!")
print(f"📘 Total Topics: {local_data['progress_summary']['total_topics']}")
print(f"📗 Completed Topics: {local_data['progress_summary']['completed_topics_count']}")
print(f"📊 Readiness: {local_data['progress_summary']['readiness_percentage']}%")
