from pathlib import Path
from app.uploads.models.response import UploadFileResponse

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

def save_upload(filename: str, content: str) -> UploadFileResponse:
	try:
		file_path = UPLOADS_DIR / filename
		file_path.write_text(content)
		return UploadFileResponse(status="ok")
	except Exception as e:
		return UploadFileResponse(error=str(e))
