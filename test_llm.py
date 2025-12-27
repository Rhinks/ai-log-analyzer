from app.utils.log_parser import parse_log
from app.utils.llm_analyzer import analyze_logs

# Read sample logs
with open("app/data/Linux_2k.log") as f:
    content = "".join(f.readlines()[-500:])


# Parse
parsed = parse_log(content)
print(f"Parsed {len(parsed)} logs")

# Analyze (calls OpenAI API)
analysis = analyze_logs(parsed)
print(analysis)