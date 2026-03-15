from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ExecutionLog(BaseModel):
    """Single log entry during execution"""
    timestamp: str
    type: str  # 'command_start', 'command_complete', 'message', 'status'
    content: str
    details: Optional[dict] = None


class ExecutionMetadata(BaseModel):
    """Metadata for an agent execution"""
    execution_id: str
    agent_name: str
    prompt: str
    status: str  # 'running', 'completed', 'failed'
    return_code: Optional[int] = None
    started_at: str
    completed_at: Optional[str] = None
    duration_seconds: Optional[float] = None


class ExecutionDetail(BaseModel):
    """Complete execution details with logs"""
    metadata: ExecutionMetadata
    logs: List[ExecutionLog]


class ExecutionSummary(BaseModel):
    """Summary of an execution for list view"""
    execution_id: str
    prompt: str
    status: str
    started_at: str
    completed_at: Optional[str] = None
    duration_seconds: Optional[float] = None


class AgentExecutionList(BaseModel):
    """List of executions for an agent"""
    agent_name: str
    executions: List[ExecutionSummary]
