from pydantic import BaseModel

# Shared base model for chat component
class ChatBaseModel(BaseModel):
	class Config:
		orm_mode = True
