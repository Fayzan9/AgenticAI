from fastapi import APIRouter
from app.settings.settings import (
	get_settings, 
	update_settings, 
	get_config, 
	update_config,
	get_workflow_files,
	update_workflow_file
)
from app.settings.models.request import (
	GetSettingsRequest, 
	UpdateSettingsRequest,
	UpdateConfigRequest,
	UpdateWorkflowFileRequest
)
from app.settings.models.response import (
	GetSettingsResponse, 
	UpdateSettingsResponse,
	GetConfigResponse,
	UpdateConfigResponse,
	GetWorkflowFilesResponse,
	UpdateWorkflowFileResponse
)

router = APIRouter()

@router.get("/settings", response_model=GetSettingsResponse)
def api_get_settings(section: str = None):
	return get_settings(section)

@router.post("/settings/update", response_model=UpdateSettingsResponse)
def api_update_settings(request: UpdateSettingsRequest):
	return update_settings(request.section, request.values)

@router.get("/settings/config", response_model=GetConfigResponse)
def api_get_config():
	"""Get all configuration values from config.py"""
	return get_config()

@router.post("/settings/config/update", response_model=UpdateConfigResponse)
def api_update_config(request: UpdateConfigRequest):
	"""Update a specific configuration value"""
	return update_config(request.key, request.value)

@router.get("/settings/workflow", response_model=GetWorkflowFilesResponse)
def api_get_workflow_files():
	"""Get all workflow template files"""
	return get_workflow_files()

@router.post("/settings/workflow/update", response_model=UpdateWorkflowFileResponse)
def api_update_workflow_file(request: UpdateWorkflowFileRequest):
	"""Update a workflow template file"""
	return update_workflow_file(request.filename, request.content)
