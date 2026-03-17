import logging
from datetime import datetime
from typing import Optional
from fastapi.responses import StreamingResponse
from services.streaming import stream_codex
from app.agent_executions.service import create_execution, add_execution_log, complete_execution
from app.agent_executions.models import ExecutionLog
from services.utils import insert_user_request
from config import AGENT_FILE_PATH, ENABLE_CONTAINER_EXECUTION

logger = logging.getLogger(__name__)

# Import container executor if enabled
container_executor = None
if ENABLE_CONTAINER_EXECUTION:
    try:
        from app.container import ContainerExecutor
        container_executor = ContainerExecutor()
        logger.info("Container execution enabled")
    except ImportError as e:
        logger.warning(f"Container execution enabled but import failed: {e}")
        container_executor = None


def run_agent_stream(usecase_name: str, user_prompt: str, thread_id: Optional[str] = None) -> StreamingResponse:
    """Execute an agent with the given prompt and stream the results."""
    
    # Create execution record and get execution_id
    execution_id = create_execution(usecase_name, user_prompt)
    
    logger.info(f"Running agent '{usecase_name}' with execution_id {execution_id}")
    
    # Choose execution method
    if ENABLE_CONTAINER_EXECUTION and container_executor:
        logger.info("Using container execution")
        return StreamingResponse(
            stream_container_execution(
                container_executor,
                usecase_name,
                execution_id,
                user_prompt,
                thread_id
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        logger.info("Using direct execution")

        prompt = insert_user_request(AGENT_FILE_PATH, user_prompt, execution_id)
        
        return StreamingResponse(
            stream_codex(
                prompt, 
                agent_name=usecase_name,
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


def stream_container_execution(
    executor,
    agent_name: str,
    execution_id: str,
    user_prompt: str,
    thread_id: Optional[str] = None
):
    """Stream container execution output as SSE events."""
    try:
        # Execute in container and stream output
        for line in executor.execute_agent(agent_name, execution_id, user_prompt):
            # Log execution
            log = ExecutionLog(
                timestamp=datetime.now().isoformat(),
                type="output",
                content=line
            )
            add_execution_log(agent_name, execution_id, log)
            
            # Format as SSE
            yield f"data: {line}\n\n"
        
        # Mark as completed
        complete_execution(agent_name, execution_id, 0)
        yield f'data: {{"type": "returncode", "code": 0}}\n\n'
        
    except Exception as e:
        logger.exception("Container execution failed")
        complete_execution(agent_name, execution_id, 1)
        yield f'data: {{"type": "error", "message": "{str(e)}"}}\n\n'
