import logging
from fastapi import APIRouter
from app.threads.threads import (
    create_thread_service, 
    list_threads_service, 
    get_thread_service, 
    add_message_to_thread_service,
    delete_thread_service
)
from app.threads.models.request import ThreadCreateRequest, MessageAddRequest
from app.threads.models.base import ThreadListResponse, Thread

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/threads", response_model=Thread)
def create_thread(request: ThreadCreateRequest):
    """Create a new thread"""
    logger.info(f"Creating new thread with title: {request.title}")
    return create_thread_service(request.title)

@router.get("/threads", response_model=ThreadListResponse)
def list_threads():
    """Get all threads, sorted by updated_at (newest first)"""
    logger.info("Fetching all threads")
    return list_threads_service()

@router.get("/threads/{thread_id}", response_model=Thread)
def get_thread(thread_id: str):
    """Get a specific thread by ID"""
    logger.info(f"Fetching thread {thread_id}")
    return get_thread_service(thread_id)

@router.post("/threads/{thread_id}/messages", response_model=Thread)
def add_message_to_thread(thread_id: str, request: MessageAddRequest):
    """Add a message to a thread"""
    logger.info(f"Adding {request.role} message to thread {thread_id}")
    return add_message_to_thread_service(
        thread_id=thread_id, 
        role=request.role, 
        text=request.text, 
        thinking_logs=request.thinking_logs
    )

@router.delete("/threads/{thread_id}")
def delete_thread_route(thread_id: str):
    """Delete a thread"""
    logger.info(f"Deleting thread {thread_id}")
    return delete_thread_service(thread_id)
