from typing import Optional, Dict, Any, List
from app.settings.models.response import (
	GetSettingsResponse, 
	UpdateSettingsResponse,
	GetConfigResponse,
	UpdateConfigResponse,
	GetWorkflowFilesResponse,
	WorkflowFileResponse,
	UpdateWorkflowFileResponse
)
from app.settings.config_manager import ConfigManager
from app.settings.workflow_manager import WorkflowManager

# In-memory settings store for demonstration (replace with persistent storage in production)
_SETTINGS = {
	"general": {"theme": "light", "language": "en"},
	"notifications": {"email": True, "sms": False}
}

# Initialize managers
config_manager = ConfigManager()
workflow_manager = WorkflowManager()


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


def get_config() -> GetConfigResponse:
	"""Get all configuration values from config.py"""
	configs = config_manager.get_all_configs()
	return GetConfigResponse(configs=configs)


def update_config(key: str, value: Any) -> UpdateConfigResponse:
	"""Update a specific configuration value"""
	success = config_manager.update_config(key, value)
	
	if success:
		return UpdateConfigResponse(success=True, message="Configuration updated successfully")
	else:
		return UpdateConfigResponse(success=False, message="Failed to update configuration")


def get_workflow_files() -> GetWorkflowFilesResponse:
	"""Get all workflow template files"""
	workflow_files = workflow_manager.get_all_files()
	files = [WorkflowFileResponse(name=f.name, content=f.content) for f in workflow_files]
	return GetWorkflowFilesResponse(files=files)


def update_workflow_file(filename: str, content: str) -> UpdateWorkflowFileResponse:
	"""Update a workflow template file"""
	success = workflow_manager.update_file(filename, content)
	
	if success:
		return UpdateWorkflowFileResponse(success=True, message="Workflow file updated successfully")
	else:
		return UpdateWorkflowFileResponse(success=False, message="Failed to update workflow file")
