from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from app.uploads.upload import save_uploads
from app.uploads.models.response import UploadFileResponse

router = APIRouter()

@router.post("/uploads", response_model=UploadFileResponse)
async def api_upload_files(
    thread_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    return await save_uploads(thread_id, files)