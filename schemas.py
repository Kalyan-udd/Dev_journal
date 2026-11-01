from pydantic import BaseModel

#TODO
class Journal(BaseModel):
    title: str
    content: str
    tags: str
    comment : list[str] = []

#TODO
class Comments(BaseModel):
    content: str