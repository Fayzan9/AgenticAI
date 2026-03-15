from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.chat.chat import process_chat_stream
from app.chat.models.request import ChatRequest
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat")
def chat_stream(request: ChatRequest):
    """Stream Codex exec JSON events as Server-Sent Events."""
    logger.info(f"Received chat request with prompt length: {len(request.prompt)} characters")
    return process_chat_stream(request)
