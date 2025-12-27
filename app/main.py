# orchestrate everything
from app.utils.llm_analyzer import analyze_logs
from collections import deque
import json

def read_last_n_lines(file_path: str, n: int = 50) -> str:
    with open(file_path, "r", errors="ignore") as f:
        return "".join(deque(f, maxlen=n))

def analyze_log_file(file_path: str) -> dict:

    content = read_last_n_lines(file_path, n=50)
    analysis = analyze_logs(content)
    return analysis


if __name__ == "__main__":
    result = analyze_log_file("app/data/Linux_2k.log")
    print(json.dumps(result, indent=2))