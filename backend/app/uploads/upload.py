from pathlib import Path
from fastapi import UploadFile
from typing import List
from app.uploads.models.response import UploadFileResponse
import shutil

DATA_FILES_DIR = Path("data/files")

async def save_uploads(thread_id: str, files: List[UploadFile]) -> UploadFileResponse:
    try:
        thread_dir = DATA_FILES_DIR / thread_id
        thread_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            file_path = thread_dir / file.filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
        return UploadFileResponse(status="ok")
    except Exception as e:
        return UploadFileResponse(error=str(e))
