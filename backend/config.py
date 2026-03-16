"""
config.py: Centralized configuration for FastAPI app
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path to UI (server is in agent/server/, UI is in agent/ui/)

# Parent directory of the current file (server/)
BASE_DIR = Path(__file__).resolve().parent

WORKFLOW_DIR = BASE_DIR / "workflow"
AGENT_DIR = WORKFLOW_DIR / "usecases"
AGENT_FILE_PATH = WORKFLOW_DIR / "AGENT.md"
MEMORY_FILE_PATH = WORKFLOW_DIR / "MEMORY.md"
UTILITIES_FILE_PATH = WORKFLOW_DIR / "UTILITIES.md"
EXECUTIONS_DIR = WORKFLOW_DIR / "executions"

DATA_DIR = BASE_DIR / "data"
THREADS_DIR = DATA_DIR / "threads"
FILES_DIR = DATA_DIR / "files"

CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Container execution settings
ENABLE_CONTAINER_EXECUTION = os.getenv("ENABLE_CONTAINER_EXECUTION", "false").lower() == "true"
ACCESS_TO_INTERNET = os.getenv("ACCESS_TO_INTERNET", "false").lower() == "true"