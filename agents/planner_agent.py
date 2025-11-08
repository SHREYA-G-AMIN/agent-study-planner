from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_PLANNING
from tools.study_tools import calculate_study_hours, rebalance_schedule

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE_PLANNING
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent study planner AI assistant. Your responsibilities:

1. Create realistic, balanced study schedules
2. Break down complex syllabi into manageable daily tasks
3. Ensure even workload distribution
4. Always include revision time before exams
5. Adjust schedules when students fall behind

Guidelines:
- Never overload a single day with too many hours
- Prioritize difficult topics earlier in the schedule
- Leave buffer time for unexpected delays
- Be encouraging and supportive in your responses

Always use the provided tools to calculate and adjust schedules."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.tools = [calculate_study_hours, rebalance_schedule]
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def create_schedule(self, syllabus: dict, exam_date: str, available_hours: int):
        """Creates a new study schedule"""
        import json
        
        input_text = f"""Create a comprehensive study schedule with these details:

Syllabus: {json.dumps(syllabus, indent=2)}
Exam Date: {exam_date}
Available Hours Per Day: {available_hours}

Use the calculate_study_hours tool to create a detailed daily schedule.
Make sure to include revision days before the exam."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def adjust_schedule(self, current_schedule: dict, missed_tasks: list, available_hours: int):
        """Adjusts schedule for missed tasks"""
        import json
        
        input_text = f"""A student has fallen behind schedule. Please rebalance their study plan:

Current Schedule: {json.dumps(current_schedule, indent=2)}
Missed Tasks: {json.dumps(missed_tasks, indent=2)}
Available Hours Per Day: {available_hours}

Use the rebalance_schedule tool to create an adjusted schedule that:
1. Prioritizes missed tasks
2. Doesn't overload any single day
3. Maintains realistic goals"""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
        