# 🎓 How to Use Your Study Planner

## 📊 Current State: What You Have

### ✅ **TWO WAYS TO USE IT:**

---

## 1️⃣ **INTERACTIVE MODE** (Takes User Input) 🆕

Run the interactive planner:
```bash
python interactive_planner.py
```

### Features:
- ✅ **Create New Study Plan** - Input your own data
- ✅ **Update Progress** - Mark topics as completed
- ✅ **View Summary** - See your progress

### Example Session:
```
🎓 STUDY PLANNER MENU
1. Create New Study Plan
2. Update Progress  
3. View Summary
4. Exit

Select option: 1

What's your name? John
Student ID: 12345

Topic 1 - Subject: Mathematics
Topic 1 - Topic name: Calculus
Topic 1 - Estimated hours: 5
Topic 1 - Start date: 2025-11-10

Topic 2 - Subject: done

✅ STUDY PLAN CREATED!
👤 Student: John
📚 Total Topics: 1
📅 Exam Date: 2025-12-10
```

---

## 2️⃣ **PROGRAMMATIC MODE** (From Code)

Use the JSON manager directly in your code:

```python
from json_manager import StudentDataManager

manager = StudentDataManager()

# Get current student data
summary = manager.get_summary()
print(f"Readiness: {summary['readiness']}%")

# Mark topic completed
manager.mark_topic_completed("Algebra")

# Add new topic
manager.add_topic_to_plan(
    date="2025-11-15",
    subject="Math", 
    topic="Calculus",
    hours=3
)

# Update streak
manager.update_streak(5)

# Get pending topics
pending = manager.get_pending_topics()
for topic in pending:
    print(f"- {topic['topic']}")
```

---

## 📁 Data Storage

All data is saved in: **`student_study_data.json`**

### Current Data Structure:
```json
{
  "student_id": 1,
  "student_name": "Sher",
  "study_plan": [
    {
      "date": "2025-10-23",
      "subject": "Maths",
      "topic": "Algebra",
      "hours": 3,
      "completed": false,
      "completed_at": null
    }
  ],
  "progress_summary": {
    "total_topics": 3,
    "completed_topics_count": 0,
    "readiness_percentage": 0.0
  },
  "current_streak": 7
}
```

---

## 🚀 Quick Start

### Option A: Use Existing Data (Mock Data)
```bash
python interactive_planner.py
# Select option 3 to view Sher's data
```

### Option B: Create Your Own Plan
```bash
python interactive_planner.py
# Select option 1 to create new plan
# Enter your name and topics
```

### Option C: Use in Your Code
```python
from json_manager import StudentDataManager
manager = StudentDataManager()
summary = manager.get_summary()
```

---

## 📝 **Answer to Your Question:**

### **"Is this taking input from users?"**

**NOW: YES! Two ways:**

1. **Mock Data (Current):**
   - Uses "Sher" from `student_study_data.json`
   - Good for testing

2. **User Input (New!):**
   - Run `interactive_planner.py`
   - Enter your own name, topics, exam dates
   - Creates personalized plan

---

## 🎯 Next Steps

### To Replace Mock Data with Your Data:
```bash
python interactive_planner.py
# Choose option 1
# Enter YOUR information
```

This will **overwrite** `student_study_data.json` with your data!

### To Keep Both:
Change the filename:
```python
manager = StudentDataManager("my_plan.json")
```

---

## 💡 Summary

| Mode | Input | Use Case |
|------|-------|----------|
| **Test Data** | Mock (Sher) | Testing, demos |
| **Interactive CLI** | User types input | Quick personal use |
| **Programmatic** | Code/API | Integration, automation |
| **Web/App** | Future UI | Production app |

**You now have interactive input capability!** 🎉

Run: `python interactive_planner.py` to try it!
