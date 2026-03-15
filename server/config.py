"""
config.py: Centralized configuration for FastAPI app
"""
from pathlib import Path

# Path to UI (server is in agent/server/, UI is in agent/ui/)
UI_DIR = Path(__file__).resolve().parent.parent / "ui"
AGENTS_DIR = Path(__file__).resolve().parent / "agents" / "created_agents"
AGENT_TEMPLATE_DIR = Path(__file__).resolve().parent / "agents" / "agent_template"

CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

AGENT_PROMPT = """
You are an agent that processess the users request using agents/workflow.md guidelines

User Request:
{user_prompt}
"""