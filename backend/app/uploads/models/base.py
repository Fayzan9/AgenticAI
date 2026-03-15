from pydantic import BaseModel

# Shared base model for uploads component
class UploadBaseModel(BaseModel):
	class Config:
		orm_mode = True
