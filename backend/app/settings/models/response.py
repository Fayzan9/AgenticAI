from .base import SettingsBaseModel
from typing import Optional, Dict, Any

class GetSettingsResponse(SettingsBaseModel):
	section: Optional[str] = None
	values: Optional[Dict[str, Any]] = None
	error: Optional[str] = None

class UpdateSettingsResponse(SettingsBaseModel):
	status: Optional[str] = None
	error: Optional[str] = None
