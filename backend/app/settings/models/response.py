from .base import SettingsBaseModel
from typing import Optional, Dict, Any, List

class GetSettingsResponse(SettingsBaseModel):
	section: Optional[str] = None
	values: Optional[Dict[str, Any]] = None
	error: Optional[str] = None

class UpdateSettingsResponse(SettingsBaseModel):
	status: Optional[str] = None
	error: Optional[str] = None

class GetConfigResponse(SettingsBaseModel):
	configs: Dict[str, Any]

class UpdateConfigResponse(SettingsBaseModel):
	success: bool
	message: Optional[str] = None

class WorkflowFileResponse(SettingsBaseModel):
	name: str
	content: str

class GetWorkflowFilesResponse(SettingsBaseModel):
	files: List[WorkflowFileResponse]

class UpdateWorkflowFileResponse(SettingsBaseModel):
	success: bool
	message: Optional[str] = None
