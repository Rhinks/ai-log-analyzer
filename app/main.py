# orchestrate everything
from app.utils.llm_analyzer import analyze_logs
from collections import deque
import json

def read_last_n_lines(file_path: str, n: int = 500) -> str:
    """Read the last n lines from a file as a single string."""
    with open(file_path, "r", errors="ignore") as f:
        return "".join(deque(f, maxlen=n))


def analyze_log_file(file_path: str) -> dict:
    """Read last 500 lines from a log file and analyze with LLM."""
    content = read_last_n_lines(file_path, n=500)
    analysis = analyze_logs(content)
    return analysis


if __name__ == "__main__":
    result = analyze_log_file("app/data/Linux_2k.log")
    print(json.dumps(result, indent=2))