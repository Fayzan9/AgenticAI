"""
thread.py: Data models for thread management
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class Message(BaseModel):
    """Represents a single message in a thread"""
    role: str  # "user" or "assistant"
    text: str
    thinking_logs: List[Dict[str, Any]] = Field(default_factory=list)  # structured logs
    timestamp: datetime = Field(default_factory=datetime.now)


class Thread(BaseModel):
    """Represents a conversation thread"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "New Chat"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=list)

    def add_message(self, role: str, text: str, thinking_logs: Optional[List[str]] = None) -> Message:
        """Add a message to the thread and update timestamp"""
        message = Message(role=role, text=text, thinking_logs=thinking_logs or [])
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message

    def update_title_from_first_message(self):
        """Auto-generate title from first user message"""
        if self.title == "New Chat" and self.messages:
            first_user_msg = next((m for m in self.messages if m.role == "user"), None)
            if first_user_msg:
                # Use first 50 characters of the first user message
                self.title = first_user_msg.text[:50].strip()
                if len(first_user_msg.text) > 50:
                    self.title += "..."


class ThreadCreateRequest(BaseModel):
    """Request to create a new thread"""
    title: Optional[str] = "New Chat"


class ThreadListResponse(BaseModel):
    """Response containing list of threads"""
    threads: List[Thread]


class MessageAddRequest(BaseModel):
    """Request to add a message to a thread"""
    role: str
    text: str
    thinking_logs: Optional[List[str]] = None
