from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from app.main import analyze_log_file
import os

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.post("/analyze")
async def analyze_logs_endpoint(file: UploadFile):
    temp_file_path = f"temp_{file.filename}"

    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
            print(f"File saved: {temp_file_path}")
            print(f"File size: {os.path.getsize(temp_file_path)}")

        result = analyze_log_file(temp_file_path)

        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
