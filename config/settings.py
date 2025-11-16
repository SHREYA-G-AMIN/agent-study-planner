import os
from dotenv import load_dotenv

load_dotenv()

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
MODEL_NAME = os.getenv("POLLINATIONS_MODEL", "openai")  # Pollinations.ai model name (default: "openai")
TEMPERATURE_PLANNING = 0.7
TEMPERATURE_TRACKING = 0.7
TEMPERATURE_MOTIVATION = 0.7
