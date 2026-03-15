from .base import UploadBaseModel
from typing import Optional

class UploadFileRequest(UploadBaseModel):
	filename: str
	content: str  # base64 or plain text for demo
