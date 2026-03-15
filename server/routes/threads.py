"""
threads.py: API routes for thread management
"""
import logging
from typing import List
from fastapi import APIRouter, HTTPException
from models.thread import Thread, ThreadCreateRequest, ThreadListResponse, MessageAddRequest
from services.thread_storage import get_thread_storage

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/threads", response_model=Thread)
def create_thread(request: ThreadCreateRequest):
    """Create a new thread"""
    logger.info(f"Creating new thread with title: {request.title}")
    
    try:
        storage = get_thread_storage()
        thread = storage.create_thread(title=request.title or "New Chat")
        logger.info(f"Successfully created thread {thread.id}")
        return thread
    except Exception as e:
        logger.error(f"Error creating thread: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create thread: {str(e)}")


@router.get("/threads", response_model=ThreadListResponse)
def list_threads():
    """Get all threads, sorted by updated_at (newest first)"""
    logger.info("Fetching all threads")
    
    try:
        storage = get_thread_storage()
        threads = storage.list_threads()
        logger.info(f"Retrieved {len(threads)} threads")
        return ThreadListResponse(threads=threads)
    except Exception as e:
        logger.error(f"Error listing threads: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list threads: {str(e)}")


@router.get("/threads/{thread_id}", response_model=Thread)
def get_thread(thread_id: str):
    """Get a specific thread by ID"""
    logger.info(f"Fetching thread {thread_id}")
    
    try:
        storage = get_thread_storage()
        thread = storage.load_thread(thread_id)
        
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


@router.post("/threads/{thread_id}/messages", response_model=Thread)
def add_message_to_thread(thread_id: str, request: MessageAddRequest):
    """Add a message to a thread"""
    logger.info(f"Adding {request.role} message to thread {thread_id}")
    
    try:
        storage = get_thread_storage()
        thread = storage.add_message_to_thread(thread_id, request.role, request.text)
        
        if not thread:
            logger.warning(f"Thread {thread_id} not found")
            raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")
        
        logger.info(f"Successfully added message to thread {thread_id}")
        return thread
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding message to thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to add message: {str(e)}")


@router.delete("/threads/{thread_id}")
def delete_thread(thread_id: str):
    """Delete a thread"""
    logger.info(f"Deleting thread {thread_id}")
    
    try:
        storage = get_thread_storage()
        success = storage.delete_thread(thread_id)
        
        if not success:
            logger.warning(f"Thread {thread_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")
        
        logger.info(f"Successfully deleted thread {thread_id}")
        return {"message": f"Thread {thread_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete thread: {str(e)}")
