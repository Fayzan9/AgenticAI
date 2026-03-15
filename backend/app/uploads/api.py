from fastapi import APIRouter
from app.uploads.upload import save_upload
from app.uploads.models.request import UploadFileRequest
from app.uploads.models.response import UploadFileResponse

router = APIRouter()

@router.post("/uploads", response_model=UploadFileResponse)
def api_upload_file(request: UploadFileRequest):
	return save_upload(request.filename, request.content)
