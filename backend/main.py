""" 
main.py: FastAPI application entry point
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from app.chat.api import router as chat_router
from app.agent.api import router as agent_router
from app.agent_explorer.api import router as explorer_router
from app.agent_executions.api import router as executions_router
from app.threads.api import router as threads_router
from app.settings.api import router as settings_router
from app.uploads.api import router as uploads_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Agent API", version="0.1.0")

logger.info("Starting Agent API server...")

# Configure CORS
logger.info(f"Configuring CORS with origins: {CORS_ORIGINS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)



@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# Register routers
logger.info("Registering API routers...")
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(threads_router, prefix="/api", tags=["Threads"])
app.include_router(agent_router, prefix="/api", tags=["Agent Operations"])
app.include_router(explorer_router, prefix="/api", tags=["Agent Management"])
app.include_router(executions_router, prefix="/api", tags=["Agent Executions"])
app.include_router(settings_router, prefix="/api", tags=["Settings"])
app.include_router(uploads_router, prefix="/api", tags=["Uploads"])

logger.info("Agent API server started successfully")
