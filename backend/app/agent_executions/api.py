"""
API endpoints for agent execution history
"""
from fastapi import APIRouter, HTTPException
from app.agent_executions.service import (
    get_all_agents_with_executions,
    get_agent_executions,
    get_execution_detail
)
from app.agent_executions.models import AgentExecutionList, ExecutionDetail
from typing import List, Dict

router = APIRouter()


@router.get("/agent-executions", response_model=List[Dict])
def list_agents_with_executions():
    """List all agents that have execution history"""
    return get_all_agents_with_executions()


@router.get("/agent-executions/{agent_name}", response_model=AgentExecutionList)
def list_agent_executions(agent_name: str):
    """List all executions for a specific agent"""
    return get_agent_executions(agent_name)


@router.get("/agent-executions/{agent_name}/{execution_id}", response_model=ExecutionDetail)
def get_execution_details(agent_name: str, execution_id: str):
    """Get detailed information about a specific execution"""
    detail = get_execution_detail(agent_name, execution_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Execution not found")
    return detail
