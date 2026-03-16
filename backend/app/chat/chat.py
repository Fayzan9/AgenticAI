import logging
from typing import Optional
from fastapi.responses import StreamingResponse
from services.streaming import stream_codex_events
from services.utils import insert_user_request
# Import message logic directly from the new threads module!
from app.threads.threads import add_message_to_thread_service
from app.chat.models.request import ChatRequest
from config import AGENT_FILE_PATH

logger = logging.getLogger(__name__)

def process_chat_stream(request: ChatRequest) -> StreamingResponse:
    if request.thread_id:
        logger.info(f"Saving user message to thread {request.thread_id}")
        try:
            add_message_to_thread_service(
                thread_id=request.thread_id, 
                role="user", 
                text=request.prompt
            )
        except Exception as e:
            logger.error(f"Error saving user message to thread: {str(e)}", exc_info=True)
    
    # Format the prompt with the agent template
    prompt = insert_user_request(AGENT_FILE_PATH, request.prompt)
    
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
