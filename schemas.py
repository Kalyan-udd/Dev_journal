from pydantic import BaseModel, field_validator

#TODO
class Journal(BaseModel):
    title: str
    content: str
    tags: str
    comment : list[str] = []

#TODO
class Comments(BaseModel):
    content: str

#TODO
class TextGenerationModel(BaseModel):
    journal_name : str
    user_prompt: str

#TODO
class ContentUpdate(BaseModel):
    content: str
