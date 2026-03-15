""" 
main.py: FastAPI application entry point
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import UI_DIR, CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from routes.chat import router as chat_router
from routes.agent import router as agent_router
from routes.agents_organizer import router as agents_organizer_router
from routes.threads import router as threads_router

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


@app.get("/")
def root():
    """Serve the chat UI."""
    index = UI_DIR / "code.html"
    if not index.exists():
        return {"message": "Hello, World!", "ui_missing": str(index)}
    return FileResponse(index)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# Register routers
logger.info("Registering API routers...")
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(threads_router, prefix="/api", tags=["Threads"])
app.include_router(agent_router, prefix="/api", tags=["Agent Operations"])
app.include_router(agents_organizer_router, prefix="/api", tags=["Agent Management"])

logger.info("Agent API server started successfully")
