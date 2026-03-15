from .base import ExplorerBaseModel
from typing import Optional, List

class ExplorerFileItem(ExplorerBaseModel):
	name: str
	path: str
	type: str  # "file" or "directory"
	children: Optional[List['ExplorerFileItem']] = None

class ExplorerListResponse(ExplorerBaseModel):
	items: Optional[List[ExplorerFileItem]] = None
	error: Optional[str] = None

class ExplorerFileContentResponse(ExplorerBaseModel):
	content: Optional[str] = None
	error: Optional[str] = None
