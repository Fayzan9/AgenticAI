import logging
from datetime import datetime
from typing import Optional
from fastapi.responses import StreamingResponse
from services.streaming import stream_codex_events
from config import RUN_STANDALONE_AGENT_PROMPT

logger = logging.getLogger(__name__)

def run_agent_stream(agent_name: str, user_prompt: str, thread_id: Optional[str] = None) -> StreamingResponse:
    """Execute an agent with the given prompt and stream the results."""
    
    # Generate timestamp for output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Format the standalone agent prompt
    prompt = RUN_STANDALONE_AGENT_PROMPT.format(
        agent_name=agent_name,
        timestamp=timestamp,
        user_prompt=user_prompt
    )
    
    logger.info(f"Running agent '{agent_name}' with timestamp {timestamp}")
    
    return StreamingResponse(
        stream_codex_events(prompt, thread_id=thread_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
