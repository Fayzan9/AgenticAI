#!/usr/bin/env python3
"""
Container entrypoint for agent execution.
Reads agent spec, executes via Codex CLI, writes output.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


def log(message: str):
    """Simple logging to stderr."""
    print(f"[CONTAINER] {message}", file=sys.stderr, flush=True)


def execute_agent():
    """Main execution function."""
    # Get environment variables
    agent_name = os.environ.get("AGENT_NAME")
    execution_id = os.environ.get("EXECUTION_ID")
    user_prompt = os.environ.get("USER_PROMPT")
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not all([agent_name, execution_id, user_prompt]):
        log("ERROR: Missing required environment variables")
        return 1
    
    # Debug: Check container user and permissions
    log(f"Container user: {os.getuid()}:{os.getgid()}")
    
    # Check authentication method
    codex_auth_file = Path.home() / ".codex" / "auth.json"
    if codex_auth_file.exists():
        log(f"Using codex auth.json from host (mounted at {codex_auth_file})")
        api_key = None  # Not needed when using auth.json
    elif api_key:
        masked_key = api_key[:10] + '...' if len(api_key) > 10 else '***'
        log(f"OPENAI_API_KEY received in container: {masked_key}")
        log("WARNING: Codex CLI does not use OPENAI_API_KEY directly. Run 'codex login' on host.")
    else:
        log("ERROR: No authentication found. Run 'codex login' on the host machine.")
        return 1
    
    log(f"Starting execution: agent={agent_name}, execution_id={execution_id}")
    
    # Paths
    agent_dir = Path(f"/workspace/agents/{agent_name}")
    execution_dir = Path(f"/workspace/executions/{agent_name}/{execution_id}")
    
    # Validate paths
    if not agent_dir.exists():
        log(f"ERROR: Agent directory not found: {agent_dir}")
        return 1
    
    if not execution_dir.exists():
        log(f"ERROR: Execution directory not found: {execution_dir}")
        return 1
    
    # Check execution directory permissions
    log(f"Execution dir permissions: {oct(os.stat(execution_dir).st_mode)[-3:]}")
    try:
        test_file = execution_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        log("Write permission test: OK")
    except Exception as e:
        log(f"Write permission test: FAILED - {e}")
    
    # Read agent specification
    agent_spec_path = agent_dir / "agent.md"
    if not agent_spec_path.exists():
        log(f"ERROR: Agent spec not found: {agent_spec_path}")
        return 1
    
    agent_spec = agent_spec_path.read_text()
    
    # Read output specification
    output_spec_path = agent_dir / "outputs" / "output_details.md"
    output_spec = ""
    if output_spec_path.exists():
        output_spec = output_spec_path.read_text()
    
    # Build prompt for Codex CLI
    prompt = f"""
You are executing the {agent_name} agent.

# Agent Instructions
{agent_spec}

# Output Format
{output_spec}

# Execution Context
execution_id: {execution_id}
output_path: {execution_dir}/output.json
metadata_path: {execution_dir}/metadata.json

# User Request
{user_prompt}

# Instructions
1. Process the user request according to the agent instructions
2. Generate the output in the specified format
3. Write the output to: {execution_dir}/output.json
4. Update metadata at: {execution_dir}/metadata.json with:
   - status: "completed"
   - return_code: 0
   - completed_at: current timestamp
   - duration_seconds: execution time

Execute immediately. All paths are pre-created.
"""
    
    # Execute with Codex CLI
    log("Executing agent via Codex CLI")
    log(f"Working directory: /workspace")
    log(f"Codex command: codex exec --json --full-auto --skip-git-repo-check")
    
    # Clear any cached codex login tokens that might conflict
    log("Clearing any cached codex logout state...")
    try:
        subprocess.run(["codex", "logout"], capture_output=True, timeout=5)
    except Exception:
        pass  # Ignore errors if no login exists
    
    try:
        result = subprocess.run(
            [
                "codex",
                "exec",
                "--json",
                "--full-auto",
                "--skip-git-repo-check",
                "-C", "/workspace",
                prompt
            ],
            capture_output=False,  # Stream to stdout/stderr
            text=True,
            timeout=300,  # 5 min timeout
        )
        
        if result.returncode != 0:
            log(f"ERROR: Codex execution failed with code {result.returncode}")
            mark_execution_failed(execution_dir, result.returncode)
            return result.returncode
        
        log("Agent execution completed successfully")
        return 0
        
    except subprocess.TimeoutExpired:
        log("ERROR: Execution timeout")
        mark_execution_failed(execution_dir, 124)
        return 124
    except Exception as e:
        log(f"ERROR: Execution failed: {e}")
        mark_execution_failed(execution_dir, 1)
        return 1


def mark_execution_failed(execution_dir: Path, return_code: int):
    """Mark execution as failed in metadata."""
    try:
        metadata_path = execution_dir / "metadata.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text())
            metadata["status"] = "failed"
            metadata["return_code"] = return_code
            metadata["completed_at"] = datetime.now().isoformat()
            
            if "started_at" in metadata:
                started = datetime.fromisoformat(metadata["started_at"])
                completed = datetime.now()
                metadata["duration_seconds"] = (completed - started).total_seconds()
            
            metadata_path.write_text(json.dumps(metadata, indent=2))
    except Exception as e:
        log(f"ERROR: Failed to update metadata: {e}")


if __name__ == "__main__":
    sys.exit(execute_agent())
