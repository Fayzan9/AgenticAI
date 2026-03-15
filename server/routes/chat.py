import logging
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.streaming import stream_codex_events
from services.thread_storage import get_thread_storage
from config import AGENT_PROMPT

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    thread_id: Optional[str] = None

@router.post("/chat")
def chat_stream(request: ChatRequest):
    """Stream Codex exec JSON events as Server-Sent Events."""
    
    logger.info(f"Received chat request with prompt length: {len(request.prompt)} characters")
    
    # If thread_id is provided, save user message to thread
    if request.thread_id:
        logger.info(f"Saving user message to thread {request.thread_id}")
        try:
            storage = get_thread_storage()
            storage.add_message_to_thread(request.thread_id, "user", request.prompt)
        except Exception as e:
            logger.error(f"Error saving user message to thread: {str(e)}", exc_info=True)
    
    prompt = AGENT_PROMPT.format(user_prompt = request.prompt)
    
    logger.info("Starting streaming response...")
    
    return StreamingResponse(
        stream_codex_events(prompt, thread_id=request.thread_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
