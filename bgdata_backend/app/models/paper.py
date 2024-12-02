from pydantic import BaseModel


class Paper(BaseModel):
  abstract: str
  title: str
  references: list['Paper']
  year: str
  category: str
