import os 
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("OPENAI_API_KEY")
if not LLM_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")
LLM_MODEL = "gpt-4o-mini"

# System prompt for analyzing logs and outputting structured JSON with errors, severity, and suggestions
SYSTEM_PROMPT = "You are a log analysis assistant. Your task is to analyze the provided log entries and identify any errors, their severity levels, and provide suggestions for resolving them."
TEMPERATURE = 0.2
OUTPUT_FORMAT = {
    "errors": [
        {
            "error_message": "string",
            "severity": "string (e.g., low, medium, high)",
            "suggestion": "string"
        }
    ],
    "summary": "string or null"  # null if no errors found, otherwise summary of analysis

}

