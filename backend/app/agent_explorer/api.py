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
	agent_path = AGENTS_DIR / f"{agent_id}.md"
	# Since agents are now single files, we can just return the file itself or an empty list of children
	if agent_path.exists():
		return [{"name": f"{agent_id}.md", "path": f"{agent_id}.md", "type": "file"}]
	return []

@router.get("/agents/{agent_id}/files/{file_path:path}")
def get_file_content(agent_id: str, file_path: str):
	agent_path = AGENTS_DIR / f"{agent_id}.md"
	if file_path == f"{agent_id}.md" or file_path == "":
		return explorer.agent_get_file_content(AGENTS_DIR, f"{agent_id}.md")
	return {"error": "File not found"}

@router.post("/agents/{agent_id}/files/manage")
def create_file_or_directory(agent_id: str, request: FileManageRequest):
	return {"error": "Not supported in new agent structure"}

@router.post("/agents/{agent_id}/files/{file_path:path}")
def save_file_content(agent_id: str, file_path: str, request: FileContentRequest, background_tasks: BackgroundTasks):
	agent_path = AGENTS_DIR / f"{agent_id}.md"
	if file_path == f"{agent_id}.md" or file_path == "":
		return explorer.agent_save_file_content(AGENTS_DIR, f"{agent_id}.md", request.content)
	return {"error": "File not found"}

@router.patch("/agents/{agent_id}/files/rename")
def rename_file_or_directory(agent_id: str, request: FileRenameRequest):
	return {"error": "Not supported in new agent structure"}

@router.delete("/agents/{agent_id}/files/{file_path:path}")
def delete_file_or_directory(agent_id: str, file_path: str):
	return {"error": "Not supported in new agent structure"}
