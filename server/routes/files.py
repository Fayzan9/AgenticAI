import logging
import os
import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, File, UploadFile, Form, HTTPException

from config import FILES_DIR

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload")
async def upload_files(
    thread_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Upload files and save them to data/files/{thread_id}"""
    logger.info(f"Received upload request for thread {thread_id} with {len(files)} files")
    
    if not thread_id:
        raise HTTPException(status_code=400, detail="thread_id is required")

    try:
        # Create directory for the thread if it doesn't exist
        thread_dir = FILES_DIR / thread_id
        thread_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        for file in files:
            file_path = thread_dir / file.filename
            
            # Save the file
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_files.append({
                "filename": file.filename,
                "path": str(file_path.relative_to(FILES_DIR.parent)),
                "size": file.size
            })
            
        logger.info(f"Successfully saved {len(saved_files)} files for thread {thread_id}")
        return {
            "message": "Files uploaded successfully",
            "thread_id": thread_id,
            "files": saved_files
        }
    except Exception as e:
        logger.error(f"Error saving files: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to save files: {str(e)}")
