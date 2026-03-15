from pydantic import BaseModel

class RunAgentRequest(BaseModel):
    prompt: str
    thread_id: str = None
