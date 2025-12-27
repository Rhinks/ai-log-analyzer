# Log Analyzer

AI-powered log analyzer using OpenAI to detect errors and provide suggestions.

## Setup

```bash
export OPENAI_API_KEY="your-key"
uvicorn app.api.routes:app --reload
```

Then upload logs to `http://127.0.0.1:8000/analyze`
