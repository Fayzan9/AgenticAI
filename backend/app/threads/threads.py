import logging
import json
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import HTTPException
from config import THREADS_DIR
from app.threads.models.base import Thread, ThreadListResponse, Message

logger = logging.getLogger(__name__)

# In-memory cache
_THREADS: dict[str, Thread] = {}


def _get_thread_path(thread_id: str) -> Path:
    return THREADS_DIR / thread_id


def _save_thread(thread: Thread):
    try:
        thread_dir = _get_thread_path(thread.id)
        thread_dir.mkdir(parents=True, exist_ok=True)

        thread_file = thread_dir / "thread.json"
        tmp_file = thread_dir / "thread.tmp"

        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(thread.model_dump(mode="json"), f, indent=2)

        tmp_file.replace(thread_file)

    except Exception as e:
        logger.error(f"Failed saving thread {thread.id}: {str(e)}", exc_info=True)
        raise


def _load_thread(thread_id: str) -> Thread:
    thread_file = _get_thread_path(thread_id) / "thread.json"

    if not thread_file.exists():
        raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")

    try:
        with open(thread_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Thread(**data)

    except json.JSONDecodeError:
        logger.error(f"Corrupted thread file: {thread_id}")
        thread_file.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Corrupted thread {thread_id}")

    except Exception as e:
        logger.error(f"Failed loading thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to load thread {thread_id}")

def create_thread_service(title: Optional[str] = None) -> Thread:
    try:
        thread = Thread(title=title or "New Chat")

        _THREADS[thread.id] = thread
        _save_thread(thread)

        logger.info(f"Successfully created thread {thread.id}")
        return thread

    except Exception as e:
        logger.error(f"Error creating thread: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create thread: {str(e)}")


def list_threads_service() -> ThreadListResponse:
    try:
        threads: List[Thread] = []

        for thread_dir in THREADS_DIR.iterdir():
            if thread_dir.is_dir():
                thread_id = thread_dir.name

                try:
                    thread = _THREADS.get(thread_id)

                    if not thread:
                        thread = _load_thread(thread_id)
                        _THREADS[thread_id] = thread

                    threads.append(thread)

                except Exception as e:
                    logger.warning(f"Skipping invalid thread {thread_id}: {str(e)}")

        sorted_threads = sorted(
            threads,
            key=lambda t: t.updated_at,
            reverse=True
        )

        return ThreadListResponse(threads=sorted_threads)

    except Exception as e:
        logger.error(f"Error listing threads: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list threads: {str(e)}")


def get_thread_service(thread_id: str) -> Thread:
    try:
        thread = _THREADS.get(thread_id)

        if not thread:
            thread = _load_thread(thread_id)
            _THREADS[thread_id] = thread

        logger.info(f"Retrieved thread {thread_id}")
        return thread

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch thread: {str(e)}")


def add_message_to_thread_service(
    thread_id: str,
    role: str,
    text: str,
    thinking_logs: Optional[List[dict]] = None
) -> Thread:
    try:
        thread = get_thread_service(thread_id)

        thread.add_message(
            role=role,
            text=text,
            thinking_logs=thinking_logs
        )

        _save_thread(thread)

        logger.info(f"Successfully added message to thread {thread_id}")
        return thread

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error adding message to thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to add message: {str(e)}")


def delete_thread_service(thread_id: str) -> dict:
    try:
        thread_dir = _get_thread_path(thread_id)

        if not thread_dir.exists():
            raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")

        shutil.rmtree(thread_dir)

        _THREADS.pop(thread_id, None)

        logger.info(f"Successfully deleted thread {thread_id}")

        return {"message": f"Thread {thread_id} deleted successfully"}

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error deleting thread {thread_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete thread: {str(e)}")