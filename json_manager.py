import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
import shutil


class StudentDataManager:
    """
    Centralized manager for student study data persistence.
    Handles reading/writing student_study_data.json with backward compatibility.
    """
    
    def __init__(self, json_path: str = "student_study_data.json"):
        """
        Initialize the data manager.
        
        Args:
            json_path: Path to the JSON file (relative or absolute)
        """
        self.json_path = json_path
        self._ensure_file_exists()
    
    def _get_default_data(self) -> Dict:
        """Returns default data structure if file doesn't exist"""
        return {
            "student_id": 1,
            "student_name": "Student",
            "study_plan": [],
            "progress_summary": {
                "total_topics": 0,
                "completed_topics_count": 0,
                "readiness_percentage": 0.0
            },
            "current_streak": 0,
            "meta": {
                "version": 1,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    
    def _ensure_file_exists(self):
        """Create the JSON file with defaults if it doesn't exist"""
        if not os.path.exists(self.json_path):
            print(f"📝 Creating new student data file: {self.json_path}")
            self.save_student_data(self._get_default_data())
    
    def load_student_data(self) -> Dict:
        """
        Load student data from JSON file with error handling.
        
        Returns:
            Dict containing student data
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Ensure all required fields exist (backward compatibility)
            data = self._ensure_schema(data)
            return data
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON file corrupted: {e}")
            # Backup corrupted file
            backup_path = f"{self.json_path}.corrupt.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy(self.json_path, backup_path)
            print(f"💾 Backed up corrupted file to: {backup_path}")
            
            # Return default data
            default_data = self._get_default_data()
            self.save_student_data(default_data)
            return default_data
            
        except FileNotFoundError:
            print(f"📝 File not found, creating new: {self.json_path}")
            default_data = self._get_default_data()
            self.save_student_data(default_data)
            return default_data
    
    def _ensure_schema(self, data: Dict) -> Dict:
        """
        Ensure all required fields exist in the data.
        Adds missing fields without removing existing ones (backward compatibility).
        
        Args:
            data: Existing data dictionary
            
        Returns:
            Data with all required fields
        """
        defaults = self._get_default_data()
        
        # Add missing top-level keys
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        # Ensure progress_summary has all fields
        if "progress_summary" in data:
            for key, value in defaults["progress_summary"].items():
                if key not in data["progress_summary"]:
                    data["progress_summary"][key] = value
        
        # Ensure meta exists
        if "meta" not in data:
            data["meta"] = defaults["meta"]
        
        # Add 'completed' field to study_plan items if missing
        if "study_plan" in data:
            for item in data["study_plan"]:
                if "completed" not in item:
                    item["completed"] = False
                if "completed_at" not in item:
                    item["completed_at"] = None
        
        return data
    
    def save_student_data(self, data: Dict) -> None:
        """
        Safely save student data to JSON file.
        Uses atomic write (temp file + rename) to prevent corruption.
        
        Args:
            data: Data dictionary to save
        """
        # Update timestamp
        if "meta" not in data:
            data["meta"] = {}
        data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        # Atomic write: write to temp file first
        temp_path = f"{self.json_path}.tmp"
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # Ensure data is written to disk
            
            # Atomic replace
            os.replace(temp_path, self.json_path)
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
    
    def update_progress(self) -> Dict:
        """
        Recalculate progress metrics based on current study_plan.
        
        Returns:
            Updated data dictionary
        """
        data = self.load_student_data()
        
        study_plan = data.get("study_plan", [])
        total_topics = len(study_plan)
        completed_count = sum(1 for item in study_plan if item.get("completed", False))
        
        # Calculate readiness percentage
        readiness_percentage = round((completed_count / total_topics * 100), 2) if total_topics > 0 else 0.0
        
        # Update progress summary
        data["progress_summary"] = {
            "total_topics": total_topics,
            "completed_topics_count": completed_count,
            "readiness_percentage": readiness_percentage
        }
        
        # Save updated data
        self.save_student_data(data)
        
        print(f"📊 Progress updated: {completed_count}/{total_topics} topics ({readiness_percentage}%)")
        
        return data
    
    def mark_topic_completed(self, topic_name: str, date: Optional[str] = None) -> Dict:
        """
        Mark a specific topic as completed.
        
        Args:
            topic_name: Name of the topic to mark as completed
            date: Optional date string (YYYY-MM-DD), defaults to today
            
        Returns:
            Updated data dictionary
        """
        data = self.load_student_data()
        
        # Find and mark the topic
        topic_found = False
        for item in data.get("study_plan", []):
            if item.get("topic") == topic_name:
                item["completed"] = True
                item["completed_at"] = date or datetime.now(timezone.utc).isoformat()
                topic_found = True
                print(f"✅ Marked '{topic_name}' as completed")
                break
        
        if not topic_found:
            print(f"⚠️ Topic '{topic_name}' not found in study plan")
            return data
        
        # Update progress and save
        return self.update_progress()
    
    def mark_topic_incomplete(self, topic_name: str) -> Dict:
        """
        Mark a specific topic as incomplete (undo completion).
        
        Args:
            topic_name: Name of the topic to mark as incomplete
            
        Returns:
            Updated data dictionary
        """
        data = self.load_student_data()
        
        # Find and unmark the topic
        topic_found = False
        for item in data.get("study_plan", []):
            if item.get("topic") == topic_name:
                item["completed"] = False
                item["completed_at"] = None
                topic_found = True
                print(f"↩️ Marked '{topic_name}' as incomplete")
                break
        
        if not topic_found:
            print(f"⚠️ Topic '{topic_name}' not found in study plan")
            return data
        
        # Update progress and save
        return self.update_progress()
    
    def get_pending_topics(self) -> List[Dict]:
        """
        Get all topics that are not yet completed.
        
        Returns:
            List of pending topic dictionaries
        """
        data = self.load_student_data()
        pending = [
            item for item in data.get("study_plan", [])
            if not item.get("completed", False)
        ]
        return pending
    
    def get_completed_topics(self) -> List[Dict]:
        """
        Get all topics that have been completed.
        
        Returns:
            List of completed topic dictionaries
        """
        data = self.load_student_data()
        completed = [
            item for item in data.get("study_plan", [])
            if item.get("completed", False)
        ]
        return completed
    
    def add_topic_to_plan(self, date: str, subject: str, topic: str, hours: int) -> Dict:
        """
        Add a new topic to the study plan.
        
        Args:
            date: Date in YYYY-MM-DD format
            subject: Subject name
            topic: Topic name
            hours: Estimated hours needed
            
        Returns:
            Updated data dictionary
        """
        data = self.load_student_data()
        
        new_topic = {
            "date": date,
            "subject": subject,
            "topic": topic,
            "hours": hours,
            "completed": False,
            "completed_at": None
        }
        
        data["study_plan"].append(new_topic)
        print(f"➕ Added topic: {topic} ({subject}) on {date}")
        
        # Update progress and save
        return self.update_progress()
    
    def get_summary(self) -> Dict:
        """
        Get a summary of student progress.
        
        Returns:
            Dictionary with summary statistics
        """
        data = self.load_student_data()
        progress = data.get("progress_summary", {})
        
        return {
            "student_name": data.get("student_name", "Unknown"),
            "total_topics": progress.get("total_topics", 0),
            "completed": progress.get("completed_topics_count", 0),
            "pending": progress.get("total_topics", 0) - progress.get("completed_topics_count", 0),
            "readiness": progress.get("readiness_percentage", 0),
            "streak": data.get("current_streak", 0)
        }
    
    def update_streak(self, new_streak: int) -> Dict:
        """
        Update the student's current study streak.
        
        Args:
            new_streak: New streak value
            
        Returns:
            Updated data dictionary
        """
        data = self.load_student_data()
        data["current_streak"] = new_streak
        self.save_student_data(data)
        print(f"🔥 Streak updated: {new_streak} days")
        return data


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing StudentDataManager\n")
    print("=" * 60)
    
    # Initialize manager
    manager = StudentDataManager()
    
    # Load current data
    print("\n1️⃣ Loading current data:")
    data = manager.load_student_data()
    print(f"   Student: {data.get('student_name')}")
    print(f"   Topics in plan: {len(data.get('study_plan', []))}")
    
    # Get summary
    print("\n2️⃣ Current summary:")
    summary = manager.get_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Get pending topics
    print("\n3️⃣ Pending topics:")
    pending = manager.get_pending_topics()
    for topic in pending:
        print(f"   - {topic.get('topic')} ({topic.get('subject')})")
    
    # Get completed topics
    print("\n4️⃣ Completed topics:")
    completed = manager.get_completed_topics()
    for topic in completed:
        print(f"   - {topic.get('topic')} ({topic.get('subject')})")
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
