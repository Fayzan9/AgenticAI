import logging
from typing import List, Optional
from fastapi import HTTPException
from app.threads.models.base import Thread, ThreadListResponse, Message

logger = logging.getLogger(__name__)

# In-memory thread store for demonstration (replace with persistent storage in production)
_THREADS = {}

def create_thread_service(title: Optional[str] = None) -> Thread:
    try:
        thread = Thread(title=title or "New Chat")
        _THREADS[thread.id] = thread
        logger.info(f"Successfully created thread {thread.id}")
        return thread
    except Exception as e:
        logger.error(f"Error creating thread: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create thread: {str(e)}")

def list_threads_service() -> ThreadListResponse:
    try:
        # Sort by updated_at, newest first
        sorted_threads = sorted(_THREADS.values(), key=lambda t: t.updated_at, reverse=True)
        return ThreadListResponse(threads=sorted_threads)
    except Exception as e:
        logger.error(f"Error listing threads: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list threads: {str(e)}")

def get_thread_service(thread_id: str) -> Thread:
    try:
        thread = _THREADS.get(thread_id)
        if not thread:
            logger.warning(f"Thread {thread_id} not found")
            raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")
        logger.info(f"Retrieved thread {thread_id}")
        return thread
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch thread: {str(e)}")

def add_message_to_thread_service(thread_id: str, role: str, text: str, thinking_logs: Optional[List[dict]] = None) -> Thread:
    try:
        thread = _THREADS.get(thread_id)
        if not thread:
            logger.warning(f"Thread {thread_id} not found")
            raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")
        
        # Add the new message
        thread.add_message(role=role, text=text, thinking_logs=thinking_logs)
        
        # In-memory save just happens automatically since we mutated the object
        # If it was persistent storage, you'd save it here
        
        logger.info(f"Successfully added message to thread {thread_id}")
        return thread
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding message to thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to add message: {str(e)}")

def delete_thread_service(thread_id: str) -> dict:
    try:
        if thread_id not in _THREADS:
            logger.warning(f"Thread {thread_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")
        
        del _THREADS[thread_id]
        logger.info(f"Successfully deleted thread {thread_id}")
        return {"message": f"Thread {thread_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete thread: {str(e)}")
