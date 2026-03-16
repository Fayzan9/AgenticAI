# app/agent/api.py: API for agent CRUD and run operations
import shutil
from fastapi import APIRouter
from config import AGENT_DIR
from app.agent.models.request import RunAgentRequest
from app.agent.agent import run_agent_stream

router = APIRouter()

@router.get("/agents")
def list_agents():
	"""List all created agents."""
	if not AGENT_DIR.exists():
		return []
	return [d.name for d in AGENT_DIR.iterdir() if d.is_dir()]

@router.post("/agents")
def create_agent(request: dict):
	"""Create a new agent by copying the template."""
	name = request.get("name")
	if not name:
		return {"error": "Name is required"}
	
	new_agent_dir = AGENT_DIR / name
	
	if new_agent_dir.exists():
		return {"error": "Agent already exists"}
	
	new_agent_dir.mkdir(parents=True, exist_ok=False)
	return {"status": "ok", "name": name}

@router.patch("/agents/{agent_id}")
def rename_agent(agent_id: str, request: dict):
	"""Rename an agent directory."""
	new_name = request.get("name")
	if not new_name:
		return {"error": "New name is required"}
	old_path = AGENT_DIR / agent_id
	new_path = AGENT_DIR / new_name
	if not old_path.exists():
		return {"error": "Agent not found"}
	if new_path.exists():
		return {"error": "New name already exists"}
	old_path.rename(new_path)
	return {"status": "ok", "name": new_name}

@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: str):
	"""Delete an entire agent directory."""
	agent_path = AGENT_DIR / agent_id
	if not agent_path.exists():
		return {"error": "Agent not found"}
	shutil.rmtree(agent_path)
	return {"status": "ok"}

@router.post("/agents/{agent_id}/run")
def run_agent(agent_id: str, request: RunAgentRequest):
	"""Execute an agent with the provided prompt."""
	
	return run_agent_stream(
		usecase_name=agent_id,
		user_prompt=request.prompt,
		thread_id=request.thread_id
	)

@router.get("/agents/{agent_id}/input-form")
def get_agent_input_form(agent_id: str):
	"""Get the agent's input form HTML if it exists."""
	agent_path = AGENT_DIR / agent_id
	if not agent_path.exists():
		return {"error": "Agent not found"}
	
	input_html_path = agent_path / "inputs" / "input.html"
	if input_html_path.exists():
		return {"html": input_html_path.read_text()}
	
	return {"html": None}
