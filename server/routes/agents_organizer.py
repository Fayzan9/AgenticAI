"""
routes/agents_organizer.py: API routes for agent management (create, rename, delete agents and their files)
"""
import shutil
from fastapi import APIRouter
from pydantic import BaseModel
from config import AGENTS_DIR

router = APIRouter()


@router.get("/agents")
def list_agents():
    """List all created agents."""
    if not AGENTS_DIR.exists():
        return []
    return [d.name for d in AGENTS_DIR.iterdir() if d.is_dir()]


@router.post("/agents")
def create_agent(request: dict):
    """Create a new agent by copying the template."""
    name = request.get("name")
    if not name:
        return {"error": "Name is required"}
    
    template_dir = AGENTS_DIR.parent / "agent_template"
    new_agent_dir = AGENTS_DIR / name
    
    if new_agent_dir.exists():
        return {"error": "Agent already exists"}
    
    shutil.copytree(template_dir, new_agent_dir)
    return {"status": "ok", "name": name}


@router.patch("/agents/{agent_id}")
def rename_agent(agent_id: str, request: dict):
    """Rename an agent directory."""
    new_name = request.get("name")
    if not new_name:
        return {"error": "New name is required"}
    
    old_path = AGENTS_DIR / agent_id
    new_path = AGENTS_DIR / new_name
    
    if not old_path.exists():
        return {"error": "Agent not found"}
    if new_path.exists():
        return {"error": "New name already exists"}
    
    old_path.rename(new_path)
    return {"status": "ok", "name": new_name}


@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: str):
    """Delete an entire agent directory."""
    agent_path = AGENTS_DIR / agent_id
    if not agent_path.exists():
        return {"error": "Agent not found"}
    
    shutil.rmtree(agent_path)
    return {"status": "ok"}


