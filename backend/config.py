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
AGENT_CWD = Path(__file__).resolve().parent / "workflow_templates"
AGENTS_DIR = AGENT_CWD / "agent_created"
AGENT_TEMPLATE_DIR = AGENT_CWD / "agent_format"
EXECUTIONS_DIR = AGENT_CWD / "agent_executions"

DATA_DIR = BASE_DIR / "data"
THREADS_DIR = DATA_DIR / "threads"
FILES_DIR = DATA_DIR / "files"

CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Container execution settings
ENABLE_CONTAINER_EXECUTION = os.getenv("ENABLE_CONTAINER_EXECUTION", "false").lower() == "true"

AGENT_PROMPT = """
Hi, you are an Agentic AI that processes the users request.

# Execution Environment Schema

## Directory Structure (Pre-defined)
- Workflow templates: `workflow_templates/workflow/`
  - workflow_router.md: Main routing logic
  - agent_execution.md: Agent execution workflow
  
- Agent definitions: `workflow_templates/agent_created/{{agent_name}}/`
  - agent.md: Agent instructions and task description
  - description.md: Agent purpose and when to use it
  - inputs/input_details.md: Input parameter specifications
  - outputs/output_details.md: Output format specifications
  
- Execution artifacts: `workflow_templates/agent_executions/{{agent_name}}/{{execution_id}}/`
  - metadata.json: Execution status, timing, and metadata
  - output.json: Agent execution results
  - logs.json: Execution logs

## Data Storage
- Thread history: `data/threads/{{thread_id}}/thread.json`
- Uploaded files: `data/files/`

## Workflow Entry Point
Load workflow from: workflow_templates/workflow/workflow_router.md

## Efficiency Guidelines
- All paths above are pre-created and follow this structure
- Use `ls` only when discovering agent names in agent_created/
- Read only the files you need for the specific task
- Avoid redundant file system exploration

Thread ID: {thread_id}

User Request:
{user_prompt}
"""

RUN_STANDALONE_AGENT_PROMPT = """
Hi, you are an Agentic AI executing a pre-selected agent to process the user's request.

# Execution Context (Pre-configured)

agent_name: {agent_name}
execution_id: {execution_id}
execution_path: workflow_templates/agent_executions/{agent_name}/{execution_id}/

# Directory Structure (Pre-created)

## Agent Specification Location
workflow_templates/agent_created/{agent_name}/
├── agent.md                    # Agent instructions (read this for task details)
├── description.md              # Agent purpose
├── inputs/
│   └── input_details.md        # Input specifications
└── outputs/
    └── output_details.md       # Output format requirements

## Execution Artifacts (Your output goes here)
workflow_templates/agent_executions/{agent_name}/{execution_id}/
├── metadata.json               # Pre-created with status="running", UPDATE when done
├── logs.json                   # Pre-created empty array
└── output.json                 # YOU MUST CREATE THIS with agent results

# Required Output Schema

## output.json
Write your agent result here: workflow_templates/agent_executions/{agent_name}/{execution_id}/output.json

Format: JSON object matching the schema defined in:
workflow_templates/agent_created/{agent_name}/outputs/output_details.md

## metadata.json Updates
After completing execution, update: workflow_templates/agent_executions/{agent_name}/{execution_id}/metadata.json

Required field updates:
- status: "completed" (or "failed" if error occurs)
- return_code: 0 for success, non-zero for failure  
- completed_at: ISO 8601 timestamp (current time)
- duration_seconds: time taken to execute

# Execution Instructions

1. Read agent instructions from: workflow_templates/agent_created/{agent_name}/agent.md
2. Read output format from: workflow_templates/agent_created/{agent_name}/outputs/output_details.md
3. Process the user request according to agent instructions
4. Write result to: workflow_templates/agent_executions/{agent_name}/{execution_id}/output.json
5. Update metadata.json with completion status

# Efficiency Guidelines (IMPORTANT)

DO:
- Read only the agent files listed above (agent.md, output_details.md)
- Execute the agent task immediately after reading instructions
- Write output files directly to the specified paths

DO NOT:
- Search for or explore the workflow_templates/ directory structure (already provided above)
- Read workflow_router.md or agent_execution.md (not needed for standalone execution)
- Use find, rg, or ls to discover paths (all paths provided above)
- Verify file existence with cat before writing (paths are pre-created)
- Read example executions or other agents (focus on {agent_name} only)

Expected execution time for simple agents: <5 seconds

# Workflow Reference (if needed)
If you need workflow guidance: workflow_templates/workflow/workflow_router.md

User Request:
{user_prompt}
"""