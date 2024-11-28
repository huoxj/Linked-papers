from pydantic import BaseModel


class Paper(BaseModel):
  abstract: str
  title: str
  references: list[int]
  year: str
  category: str
