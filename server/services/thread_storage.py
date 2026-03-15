"""
thread_storage.py: Service for persisting threads to disk
"""
import json
import logging
from pathlib import Path
from typing import List, Optional
from models.thread import Thread, Message

logger = logging.getLogger(__name__)

# Get the data/threads directory
THREADS_DIR = Path(__file__).resolve().parent.parent / "data" / "threads"


class ThreadStorage:
    """Handles reading and writing thread data to JSON files"""
    
    def __init__(self, storage_dir: Path = THREADS_DIR):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"ThreadStorage initialized with directory: {self.storage_dir}")
    
    def _get_thread_file(self, thread_id: str) -> Path:
        """Get the file path for a thread"""
        return self.storage_dir / f"{thread_id}.json"
    
    def save_thread(self, thread: Thread) -> Thread:
        """Save a thread to disk"""
        file_path = self._get_thread_file(thread.id)
        
        try:
            # Convert thread to dict with datetime serialization
            thread_dict = thread.model_dump(mode='json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(thread_dict, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Saved thread {thread.id} to {file_path}")
            return thread
        except Exception as e:
            logger.error(f"Error saving thread {thread.id}: {str(e)}", exc_info=True)
            raise
    
    def load_thread(self, thread_id: str) -> Optional[Thread]:
        """Load a thread from disk"""
        file_path = self._get_thread_file(thread_id)
        
        if not file_path.exists():
            logger.warning(f"Thread file not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                thread_dict = json.load(f)
            
            thread = Thread(**thread_dict)
            logger.info(f"Loaded thread {thread_id} from {file_path}")
            return thread
        except Exception as e:
            logger.error(f"Error loading thread {thread_id}: {str(e)}", exc_info=True)
            return None
    
    def list_threads(self) -> List[Thread]:
        """List all threads, sorted by updated_at (newest first)"""
        threads = []
        
        try:
            for file_path in self.storage_dir.glob("*.json"):
                thread_id = file_path.stem
                thread = self.load_thread(thread_id)
                if thread:
                    threads.append(thread)
            
            # Sort by updated_at, newest first
            threads.sort(key=lambda t: t.updated_at, reverse=True)
            logger.info(f"Listed {len(threads)} threads")
            return threads
        except Exception as e:
            logger.error(f"Error listing threads: {str(e)}", exc_info=True)
            return []
    
    def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread from disk"""
        file_path = self._get_thread_file(thread_id)
        
        if not file_path.exists():
            logger.warning(f"Thread file not found for deletion: {file_path}")
            return False
        
        try:
            file_path.unlink()
            logger.info(f"Deleted thread {thread_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting thread {thread_id}: {str(e)}", exc_info=True)
            return False
    
    def thread_exists(self, thread_id: str) -> bool:
        """Check if a thread exists"""
        return self._get_thread_file(thread_id).exists()
    
    def create_thread(self, title: str = "New Chat") -> Thread:
        """Create a new thread and save it"""
        thread = Thread(title=title)
        self.save_thread(thread)
        logger.info(f"Created new thread {thread.id} with title: {title}")
        return thread
    
    def add_message_to_thread(self, thread_id: str, role: str, text: str) -> Optional[Thread]:
        """Add a message to an existing thread"""
        thread = self.load_thread(thread_id)
        
        if not thread:
            logger.error(f"Cannot add message: Thread {thread_id} not found")
            return None
        
        thread.add_message(role, text)
        thread.update_title_from_first_message()
        self.save_thread(thread)
        logger.info(f"Added {role} message to thread {thread_id}")
        return thread


# Global instance
_storage_instance = None


def get_thread_storage() -> ThreadStorage:
    """Get the global ThreadStorage instance"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = ThreadStorage()
    return _storage_instance
