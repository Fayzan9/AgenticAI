from fastapi import APIRouter, BackgroundTasks
from config import AGENT_CWD, AGENTS_DIR
from app.agent_explorer.models.request import (
    ExplorerListRequest, 
    ExplorerFileRequest,
    FileManageRequest,
    FileContentRequest,
    FileRenameRequest
)
from app.agent_explorer.models.response import ExplorerListResponse, ExplorerFileContentResponse
from pydantic import BaseModel
from . import explorer

router = APIRouter()

@router.get("/explorer/list", response_model=ExplorerListResponse)
def api_list_directory(path: str = None):
	items = explorer.list_directory(AGENT_CWD, path)
	return ExplorerListResponse(items=items)

@router.get("/explorer/file", response_model=ExplorerFileContentResponse)
def api_get_file_content(path: str):
	content = explorer.get_file_content(AGENT_CWD, path)
	if content is None:
		return ExplorerFileContentResponse(error="File not found")
	return ExplorerFileContentResponse(content=content)

@router.get("/agents/{agent_id}/files")
def list_agent_files(agent_id: str):
	agent_path = AGENTS_DIR / agent_id
	return explorer.agent_list_files(agent_path)

@router.get("/agents/{agent_id}/files/{file_path:path}")
def get_file_content(agent_id: str, file_path: str):
	agent_path = AGENTS_DIR / agent_id
	return explorer.agent_get_file_content(agent_path, file_path)

@router.post("/agents/{agent_id}/files/manage")
def create_file_or_directory(agent_id: str, request: FileManageRequest):
	agent_path = AGENTS_DIR / agent_id
	return explorer.agent_create_file_or_directory(agent_path, request.path, request.type)

@router.post("/agents/{agent_id}/files/{file_path:path}")
def save_file_content(agent_id: str, file_path: str, request: FileContentRequest, background_tasks: BackgroundTasks):
	agent_path = AGENTS_DIR / agent_id
	return explorer.agent_save_file_content(agent_path, file_path, request.content)

@router.patch("/agents/{agent_id}/files/rename")
def rename_file_or_directory(agent_id: str, request: FileRenameRequest):
	agent_path = AGENTS_DIR / agent_id
	return explorer.agent_rename_file_or_directory(agent_path, request.old_path, request.new_path)

@router.delete("/agents/{agent_id}/files/{file_path:path}")
def delete_file_or_directory(agent_id: str, file_path: str):
	agent_path = AGENTS_DIR / agent_id
	return explorer.agent_delete_file_or_directory(agent_path, file_path)
