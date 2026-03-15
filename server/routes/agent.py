"""
routes/agent.py: API routes for individual agent operations (files, content)
"""
from fastapi import APIRouter
from config import AGENTS_DIR
from pydantic import BaseModel
import shutil

router = APIRouter()


@router.get("/agents/{agent_id}/files")
def list_agent_files(agent_id: str):
    """List files within an agent directory recursively."""
    agent_path = AGENTS_DIR / agent_id
    if not agent_path.exists() or not agent_path.is_dir():
        return {"error": "Agent not found"}

    def get_files(path):
        items = []
        for p in path.iterdir():
            if p.name == "__pycache__":
                continue
            item = {"name": p.name, "path": str(p.relative_to(agent_path))}
            if p.is_dir():
                item["type"] = "directory"
                item["children"] = get_files(p)
            else:
                item["type"] = "file"
            items.append(item)
        return sorted(items, key=lambda x: (x["type"] != "directory", x["name"]))

    return get_files(agent_path)


@router.get("/agents/{agent_id}/files/{file_path:path}")
def get_file_content(agent_id: str, file_path: str):
    """Get the content of a specific file."""
    full_path = AGENTS_DIR / agent_id / file_path
    if not full_path.exists() or not full_path.is_file():
        return {"error": "File not found"}
    return {"content": full_path.read_text()}


class FileManageRequest(BaseModel):
    path: str
    type: str  # "file" or "directory"


@router.post("/agents/{agent_id}/files/manage")
def create_file_or_directory(agent_id: str, request: FileManageRequest):
    """Create a new file or directory within an agent."""
    agent_path = AGENTS_DIR / agent_id
    full_path = agent_path / request.path
    
    if full_path.exists():
        return {"error": "Path already exists"}
    
    if request.type == "directory":
        full_path.mkdir(parents=True, exist_ok=True)
    else:
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.touch()
    
    return {"status": "ok"}


class FileContentRequest(BaseModel):
    content: str


@router.post("/agents/{agent_id}/files/{file_path:path}")
def save_file_content(agent_id: str, file_path: str, request: FileContentRequest):
    """Save content to a specific file."""
    full_path = AGENTS_DIR / agent_id / file_path
    if not full_path.exists() or not full_path.is_file():
        return {"error": "File not found"}
    full_path.write_text(request.content)
    return {"status": "ok"}


class FileRenameRequest(BaseModel):
    old_path: str
    new_path: str


@router.patch("/agents/{agent_id}/files/rename")
def rename_file_or_directory(agent_id: str, request: FileRenameRequest):
    """Rename a file or directory within an agent."""
    agent_path = AGENTS_DIR / agent_id
    old_full_path = agent_path / request.old_path
    new_full_path = agent_path / request.new_path
    
    if not old_full_path.exists():
        return {"error": "Source path not found"}
    if new_full_path.exists():
        return {"error": "Destination path already exists"}
    
    old_full_path.rename(new_full_path)
    return {"status": "ok"}


@router.delete("/agents/{agent_id}/files/{file_path:path}")
def delete_file_or_directory(agent_id: str, file_path: str):
    """Delete a file or directory within an agent."""
    full_path = AGENTS_DIR / agent_id / file_path
    if not full_path.exists():
        return {"error": "Path not found"}
    
    if full_path.is_dir():
        shutil.rmtree(full_path)
    else:
        full_path.unlink()
    
    return {"status": "ok"}
