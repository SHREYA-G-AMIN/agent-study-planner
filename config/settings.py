import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"  # Using cheaper model for development
TEMPERATURE_PLANNING = 0.3
TEMPERATURE_TRACKING = 0.2
TEMPERATURE_MOTIVATION = 0.7
