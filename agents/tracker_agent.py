from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_TRACKING
from tools.study_tools import check_completion_status, get_progress_analytics

class TrackerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE_TRACKING
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a study progress tracking AI assistant. Your responsibilities:

1. Monitor daily task completion accurately
2. Identify patterns in student behavior
3. Calculate readiness and completion percentages
4. Detect when students are falling behind
5. Provide objective progress assessments

Guidelines:
- Be accurate and data-driven
- Identify both strengths and areas for improvement
- Alert when intervention is needed
- Track streaks and consistency

Always use the provided tools to analyze progress data."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.tools = [check_completion_status, get_progress_analytics]
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
    
    def track_progress(self, schedule: dict, completed_topics: list):
        """Tracks completion status"""
        import json
        
        completed_str = ",".join(completed_topics)
        
        input_text = f"""Analyze the student's progress:

Schedule: {json.dumps(schedule, indent=2)}
Completed Topics: {completed_str}

Use check_completion_status to analyze what's been completed and what's been missed.
Provide a clear assessment of their current standing."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def get_analytics(self, completed_count: int, missed_count: int, streak: int):
        """Gets performance analytics"""
        input_text = f"""Generate performance analytics:

Completed Tasks: {completed_count}
Missed Tasks: {missed_count}
Current Streak: {streak} days

Use get_progress_analytics to create a comprehensive performance report."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
        