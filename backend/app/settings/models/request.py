from .base import SettingsBaseModel
from typing import Optional, Dict, Any

class GetSettingsRequest(SettingsBaseModel):
	section: Optional[str] = None

class UpdateSettingsRequest(SettingsBaseModel):
	section: str
	values: Dict[str, Any]

class UpdateConfigRequest(SettingsBaseModel):
	key: str
	value: Any

class UpdateWorkflowFileRequest(SettingsBaseModel):
	filename: str
	content: str
