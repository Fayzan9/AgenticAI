import logging
from datetime import datetime
from typing import Optional
from fastapi.responses import StreamingResponse
from services.streaming import stream_codex_events_with_tracking
from app.agent_executions.service import create_execution
from config import RUN_STANDALONE_AGENT_PROMPT

logger = logging.getLogger(__name__)

def run_agent_stream(agent_name: str, user_prompt: str, thread_id: Optional[str] = None) -> StreamingResponse:
    """Execute an agent with the given prompt and stream the results."""
    
    # Create execution record and get execution_id
    execution_id = create_execution(agent_name, user_prompt)
    
    # Format the standalone agent prompt with execution_id
    prompt = RUN_STANDALONE_AGENT_PROMPT.format(
        agent_name=agent_name,
        execution_id=execution_id,
        user_prompt=user_prompt
    )
    
    logger.info(f"Running agent '{agent_name}' with execution_id {execution_id}")
    
    return StreamingResponse(
        stream_codex_events_with_tracking(
            prompt, 
            agent_name=agent_name,
            execution_id=execution_id,
            thread_id=thread_id
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
