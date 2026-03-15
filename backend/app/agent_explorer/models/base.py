from pydantic import BaseModel

# Shared base model for explorer component
class ExplorerBaseModel(BaseModel):
	class Config:
		orm_mode = True
