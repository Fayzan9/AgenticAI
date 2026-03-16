"""
Service for managing agent execution history
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
from config import EXECUTIONS_DIR
from app.agent_executions.models import (
    ExecutionMetadata,
    ExecutionLog,
    ExecutionDetail,
    ExecutionSummary,
    AgentExecutionList
)


def _ensure_executions_dir():
    """Ensure executions directory exists"""
    EXECUTIONS_DIR.mkdir(parents=True, exist_ok=True)


def create_execution(agent_name: str, prompt: str) -> str:
    """
    Create a new execution record
    Returns: execution_id
    """
    _ensure_executions_dir()
    
    execution_id = str(uuid.uuid4())
    agent_dir = EXECUTIONS_DIR / agent_name
    agent_dir.mkdir(exist_ok=True)
    
    execution_dir = agent_dir / execution_id
    execution_dir.mkdir(exist_ok=True)
    
    metadata = ExecutionMetadata(
        execution_id=execution_id,
        agent_name=agent_name,
        prompt=prompt,
        status="running",
        started_at=datetime.now().isoformat()
    )
    
    # Save metadata
    metadata_path = execution_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata.dict(), indent=2))
    
    # Initialize empty logs
    logs_path = execution_dir / "logs.json"
    logs_path.write_text(json.dumps([], indent=2))
    
    return execution_id


def add_execution_log(agent_name: str, execution_id: str, log: ExecutionLog):
    """Add a log entry to an execution"""
    execution_dir = EXECUTIONS_DIR / agent_name / execution_id
    logs_path = execution_dir / "logs.json"
    
    if not logs_path.exists():
        return
    
    logs = json.loads(logs_path.read_text())
    
    # Defensive: handle corrupted logs file
    if not isinstance(logs, list):
        logs = []
    
    logs.append(log.dict())
    logs_path.write_text(json.dumps(logs, indent=2))


def complete_execution(agent_name: str, execution_id: str, return_code: int, usage_data: Optional[dict] = None):
    """Mark execution as completed and save token usage"""
    execution_dir = EXECUTIONS_DIR / agent_name / execution_id
    metadata_path = execution_dir / "metadata.json"
    
    if not metadata_path.exists():
        return
    
    metadata = json.loads(metadata_path.read_text())
    completed_at = datetime.now().isoformat()
    
    # Defensive: handle missing started_at field
    if "started_at" not in metadata:
        # Use current time as fallback if started_at is missing
        metadata["started_at"] = completed_at
        started_at = datetime.fromisoformat(completed_at)
    else:
        started_at = datetime.fromisoformat(metadata["started_at"])
    
    completed_dt = datetime.fromisoformat(completed_at)
    
    metadata["status"] = "completed" if return_code == 0 else "failed"
    metadata["return_code"] = return_code
    metadata["completed_at"] = completed_at
    metadata["duration_seconds"] = (completed_dt - started_at).total_seconds()
    
    # Add token usage and cost if available
    if usage_data:
        from services.utils import calculate_cost
        metadata["usage"] = calculate_cost(usage_data)
    
    metadata_path.write_text(json.dumps(metadata, indent=2))


def get_all_agents_with_executions() -> List[Dict]:
    """Get list of all agents that have executions"""
    _ensure_executions_dir()
    
    agents = []
    for agent_dir in EXECUTIONS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        
        execution_count = sum(1 for x in agent_dir.iterdir() if x.is_dir())
        agents.append({
            "agent_name": agent_dir.name,
            "execution_count": execution_count
        })
    
    return sorted(agents, key=lambda x: x["agent_name"])


def get_agent_executions(agent_name: str) -> AgentExecutionList:
    """Get all executions for a specific agent"""
    agent_dir = EXECUTIONS_DIR / agent_name
    
    if not agent_dir.exists():
        return AgentExecutionList(agent_name=agent_name, executions=[])
    
    executions = []
    for execution_dir in agent_dir.iterdir():
        if not execution_dir.is_dir():
            continue
        
        metadata_path = execution_dir / "metadata.json"
        if not metadata_path.exists():
            continue
        
        metadata = json.loads(metadata_path.read_text())
        executions.append(ExecutionSummary(**metadata))
    
    # Sort by started_at descending (newest first)
    executions.sort(key=lambda x: x.started_at, reverse=True)
    
    return AgentExecutionList(agent_name=agent_name, executions=executions)


def get_execution_detail(agent_name: str, execution_id: str) -> Optional[ExecutionDetail]:
    """Get complete details of a specific execution"""
    execution_dir = EXECUTIONS_DIR / agent_name / execution_id
    
    if not execution_dir.exists():
        return None
    
    metadata_path = execution_dir / "metadata.json"
    logs_path = execution_dir / "logs.json"
    
    if not metadata_path.exists() or not logs_path.exists():
        return None
    
    metadata = ExecutionMetadata(**json.loads(metadata_path.read_text()))
    logs_data = json.loads(logs_path.read_text())
    logs = [ExecutionLog(**log) for log in logs_data]
    
    return ExecutionDetail(metadata=metadata, logs=logs)
