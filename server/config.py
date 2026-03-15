"""
config.py: Centralized configuration for FastAPI app
"""
from pathlib import Path

# Path to UI (server is in agent/server/, UI is in agent/ui/)

# Parent directory of the current file (server/)
BASE_DIR = Path(__file__).resolve().parent
# Path to UI directory
UI_DIR = Path(__file__).resolve().parent.parent / "ui"
# Path to agents working directory (agents/)
AGENT_CWD = Path(__file__).resolve().parent / "agents"
# Path to created agents directory
AGENTS_DIR = AGENT_CWD / "created_agents"
# Path to agent template directory
AGENT_TEMPLATE_DIR = BASE_DIR / "agent_template"
# Path to threads data directory
THREADS_DIR = BASE_DIR / "data" / "threads"
# Base data directory
DATA_DIR = BASE_DIR / "data"
# Path to files directory
FILES_DIR = DATA_DIR / "files"

CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

AGENT_PROMPT = """
You are an agent that processess the users request using agents/workflow.md guidelines
thread_id: {thread_id}
User Request:
{user_prompt}
"""