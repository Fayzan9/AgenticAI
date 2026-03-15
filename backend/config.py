"""
config.py: Centralized configuration for FastAPI app
"""
from pathlib import Path

# Path to UI (server is in agent/server/, UI is in agent/ui/)

# Parent directory of the current file (server/)
BASE_DIR = Path(__file__).resolve().parent
AGENT_CWD = Path(__file__).resolve().parent / "workflow_templates"
AGENTS_DIR = AGENT_CWD / "agent_created"
AGENT_TEMPLATE_DIR = AGENT_CWD / "agent_format"

DATA_DIR = BASE_DIR / "data"
THREADS_DIR = DATA_DIR / "threads"
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