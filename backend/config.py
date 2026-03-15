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
EXECUTIONS_DIR = DATA_DIR / "agent_executions"

CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

AGENT_PROMPT = """
Hi, you are an Agentic AI that processes the users request.

workflow -> workflow_templates/workflow/workflow_router.md

Thread ID: {thread_id}

User Request:
{user_prompt}
"""

RUN_STANDALONE_AGENT_PROMPT = """
Hi, you are an Agentic AI that processes the users request using the provided agent workflow.

# Workflow to Run
workflow -> workflow_templates/workflow/workflow_router.md

# Agent To Use
agent_name -> {agent_name}
agent_output_path -> workflow_templates/agent_execution/{agent_name}/{timestamp}/"

User Request:
{user_prompt}
"""