from .base import ExplorerBaseModel
from typing import Optional
from pydantic import BaseModel

class ExplorerListRequest(ExplorerBaseModel):
	path: Optional[str] = None

class ExplorerFileRequest(ExplorerBaseModel):
	path: str

class FileRenameRequest(BaseModel):
	old_path: str
	new_path: str

class FileContentRequest(BaseModel):
	content: str

class FileManageRequest(BaseModel):
	path: str
	type: str  # "file" or "directory"