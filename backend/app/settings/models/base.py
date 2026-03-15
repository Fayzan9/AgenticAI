from pydantic import BaseModel

# Shared base model for settings component
class SettingsBaseModel(BaseModel):
	class Config:
		orm_mode = True
