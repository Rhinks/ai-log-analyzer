from config import (
    LLM_MODEL,
    SYSTEM_PROMPT,
    OUTPUT_FORMAT,
    TEMPERATURE,
    LLM_API_KEY
)

from openai import OpenAI
import json

client = OpenAI(api_key=LLM_API_KEY)


def analyze_logs(parsed_logs: list[dict]) -> dict:
    """
    Input: list of parsed log dictionaries
    Output: structured JSON with errors, severity, suggestions
    """

    system_message = f"""
        {SYSTEM_PROMPT}
        
        You MUST respond in valid JSON using EXACTLY this format:
        {json.dumps(OUTPUT_FORMAT, indent=2)}
        
        Rules:
        - Do NOT add extra keys
        - Do NOT add explanations
        - If errors are found: return ONLY the 'errors' array, DO NOT include 'summary'
        - If NO errors found: return ONLY the 'summary' string, DO NOT include 'errors'
        """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": json.dumps(parsed_logs, indent=2)
            }
        ],
        temperature=TEMPERATURE,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


# Example run
if __name__ == "__main__":
    sample_parsed_logs = [
        {
            "timestamp": "Jun 15 02:04:59",
            "hostname": "combo",
            "process": "sshd(pam_unix)",
            "pid": "20885",
            "message": "authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=192.168.100 user=root"
        },
        {
            "timestamp": "Jun 15 02:05:01",
            "hostname": "combo",
            "process": "sshd",
            "pid": "20890",
            "message": "Accepted password for user from 192.168.100 port 54321 ssh2"
        }
    ]

    result = analyze_logs(sample_parsed_logs)
    print(json.dumps(result, indent=2))
