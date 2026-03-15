from typing import Optional, Dict, Any
from app.settings.models.response import GetSettingsResponse, UpdateSettingsResponse

# In-memory settings store for demonstration (replace with persistent storage in production)
_SETTINGS = {
	"general": {"theme": "light", "language": "en"},
	"notifications": {"email": True, "sms": False}
}

def get_settings(section: Optional[str] = None) -> GetSettingsResponse:
	if section:
		values = _SETTINGS.get(section)
		if values is None:
			return GetSettingsResponse(error="Section not found")
		return GetSettingsResponse(section=section, values=values)
	return GetSettingsResponse(values=_SETTINGS)

def update_settings(section: str, values: Dict[str, Any]) -> UpdateSettingsResponse:
	if section not in _SETTINGS:
		return UpdateSettingsResponse(error="Section not found")
	_SETTINGS[section].update(values)
	return UpdateSettingsResponse(status="ok")
