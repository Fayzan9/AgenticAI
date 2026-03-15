from .base import UploadBaseModel
from typing import Optional

class UploadFileResponse(UploadBaseModel):
	status: Optional[str] = None
	error: Optional[str] = None
