from pydantic import BaseModel


class Paper(BaseModel):
  id: int
  abstract: str
  title: str
  references: list['Paper']
  year: str
  category: str
