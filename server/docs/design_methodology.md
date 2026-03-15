# Design Methodology for Agent Server

## 1. Folder Structure & Modularity
- **Entry Point:** `main.py` contains only app initialization and router inclusion.
- **Configuration:** All config (paths, CORS, etc.) in `config.py`.
- **API Routes:** Each logical group of endpoints in its own file under `routes/` using FastAPI `APIRouter`.
- **Services:** Business logic, integrations, and streaming/event code in `services/`.
- **Utilities:** Shared helpers in `utils/` (add as needed).
- **Agent Definitions:** Remain in `app/` as markdown or Python as needed.

## 2. Principles
- **Single Responsibility:** Each file/module does one thing.
- **Separation of Concerns:** API, business logic, and config are separate.
- **Small Files:** No file should be monolithic; split by responsibility.
- **Explicit Imports:** Always import from the correct module, never duplicate code.
- **Type Hints:** Use Python type hints everywhere for clarity.

## 3. Adding New Features
- **New API Endpoint:**
  1. Create a new file in `routes/` (e.g., `routes/agents.py`).
  2. Define endpoints using `APIRouter`.
  3. Register the router in `main.py` with a prefix.
- **New Service/Logic:**
  1. Add a new module in `services/`.
  2. Keep logic reusable and testable.
- **Configuration:**
  1. Add new config to `config.py`.
  2. Import config where needed.

## 4. Code Style & Review
- **PEP8**: Follow Python PEP8 style guide.
- **Docstrings:** Every function/class/module should have a docstring.
- **Testing:** Write tests for all business logic (add `tests/` folder as project grows).
- **Reviews:** All code changes should be reviewed for modularity and clarity.

## 5. Example: Adding a New Route
```python
# routes/example.py
from fastapi import APIRouter
router = APIRouter()
@router.get("/example")
def example():
    return {"message": "Hello"}

# main.py
from routes.example import router as example_router
app.include_router(example_router, prefix="/api")
```

## 6. Scalability
- As the project grows, further split `services/` and `routes/` by domain.
- Move agent logic to Python modules if/when needed.
- Add `tests/` and CI for automated testing.

---
This methodology must be followed for all future development to ensure maintainability and scalability.
