from fastapi import APIRouter
from app.settings.settings import get_settings, update_settings
from app.settings.models.request import GetSettingsRequest, UpdateSettingsRequest
from app.settings.models.response import GetSettingsResponse, UpdateSettingsResponse

router = APIRouter()

@router.get("/settings", response_model=GetSettingsResponse)
def api_get_settings(section: str = None):
	return get_settings(section)

@router.post("/settings/update", response_model=UpdateSettingsResponse)
def api_update_settings(request: UpdateSettingsRequest):
	return update_settings(request.section, request.values)
