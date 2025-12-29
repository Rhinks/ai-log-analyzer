from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from app.main import analyze_log_file
from openai import OpenAIError
import os
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/")
async def root() -> FileResponse:
    return FileResponse("app/static/index.html")

@app.post("/analyze")
async def analyze_logs_endpoint(file: UploadFile) -> dict:
    """Analyze uploaded log file and return structured results or error."""
    
    # Validate file type
    allowed_extensions = {".log", ".txt"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        logger.warning(f"Invalid file type attempted: {file.filename}")
        return {
            "status": "error",
            "message": "Invalid file type. Only .log and .txt files are supported.",
            "errors": []
        }
    
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(file.filename)
    temp_file_path = f"temp_{safe_filename}"

    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        file_size = os.path.getsize(temp_file_path)
        logger.info(f"File received: {safe_filename} ({file_size} bytes)")

        # Validate file size (10MB limit)
        if file_size > 10 * 1024 * 1024:
            return {
                "status": "error",
                "message": "File too large. Maximum size is 10MB.",
                "errors": []
            }

        result = analyze_log_file(temp_file_path)
        return result

    except FileNotFoundError:
        logger.error(f"File not found: {temp_file_path}")
        return {
            "status": "error",
            "message": "File could not be read. Please try again.",
            "errors": []
        }
    
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return {
            "status": "error",
            "message": "API error. Check your OpenAI key or try again.",
            "errors": []
        }
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": "An unexpected error occurred. Please try again.",
            "errors": []
        }

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
