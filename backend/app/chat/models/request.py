from .base import ChatBaseModel
from typing import Optional

class ChatRequest(ChatBaseModel):
    prompt: str
    thread_id: Optional[str] = None
