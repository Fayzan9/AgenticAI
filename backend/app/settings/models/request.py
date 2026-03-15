from .base import SettingsBaseModel
from typing import Optional, Dict, Any

class GetSettingsRequest(SettingsBaseModel):
	section: Optional[str] = None

class UpdateSettingsRequest(SettingsBaseModel):
	section: str
	values: Dict[str, Any]
