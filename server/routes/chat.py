from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.streaming import stream_codex_events
from config import AGENT_PROMPT
router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat")
def chat_stream(request: ChatRequest):
    """Stream Codex exec JSON events as Server-Sent Events."""
    
    prompt = AGENT_PROMPT.format(user_prompt = request.prompt)
    
    return StreamingResponse(
        stream_codex_events(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
