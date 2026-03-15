# app/agent/api.py: API for agent CRUD and run operations
import shutil
from fastapi import APIRouter
from config import AGENTS_DIR, AGENT_TEMPLATE_DIR
from app.agent.models.request import RunAgentRequest
from app.agent.agent import run_agent_stream

router = APIRouter()

@router.get("/agents")
def list_agents():
	"""List all created agents."""
	if not AGENTS_DIR.exists():
		return []
	return [d.stem for d in AGENTS_DIR.glob("*.md")]

@router.post("/agents")
def create_agent(request: dict):
	"""Create a new agent by copying the template."""
	name = request.get("name")
	if not name:
		return {"error": "Name is required"}
	new_agent_file = AGENTS_DIR / f"{name}.md"
	if new_agent_file.exists():
		return {"error": "Agent already exists"}
	# If there's a template file, copy it, otherwise create empty
	template_file = AGENT_TEMPLATE_DIR / "agent_template.md"
	if template_file.exists():
		shutil.copy(template_file, new_agent_file)
	else:
		new_agent_file.write_text(f"# {name} Agent\n\nTask description here.")
	return {"status": "ok", "name": name}

@router.patch("/agents/{agent_id}")
def rename_agent(agent_id: str, request: dict):
	"""Rename an agent directory."""
	new_name = request.get("name")
	if not new_name:
		return {"error": "New name is required"}
	old_path = AGENTS_DIR / f"{agent_id}.md"
	new_path = AGENTS_DIR / f"{new_name}.md"
	if not old_path.exists():
		return {"error": "Agent not found"}
	if new_path.exists():
		return {"error": "New name already exists"}
	old_path.rename(new_path)
	return {"status": "ok", "name": new_name}

@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: str):
	"""Delete an entire agent directory."""
	agent_path = AGENTS_DIR / f"{agent_id}.md"
	if not agent_path.exists():
		return {"error": "Agent not found"}
	agent_path.unlink()
	return {"status": "ok"}

@router.post("/agents/{agent_id}/run")
def run_agent(agent_id: str, request: RunAgentRequest):
	"""Execute an agent with the provided prompt."""
	agent_path = AGENTS_DIR / f"{agent_id}.md"
	if not agent_path.exists():
		return {"error": "Agent not found"}
	
	return run_agent_stream(
		agent_name=agent_id,
		user_prompt=request.prompt,
		thread_id=request.thread_id
	)

@router.get("/agents/{agent_id}/input-form")
def get_agent_input_form(agent_id: str):
	"""Get the agent's input form HTML if it exists."""
	agent_path = AGENTS_DIR / f"{agent_id}.md"
	if not agent_path.exists():
		return {"error": "Agent not found"}
	
	# In the new structure, we might not have a separate input.html
	# For now, just return null as per original logic if not found
	return {"html": None}
