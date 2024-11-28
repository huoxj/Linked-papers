from sqlmodel import SQLModel, Field


class PaperInDB(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  abstract: str = Field(index=True)
  title: str = Field(index=True)
  references: list[int] = Field(index=True)
  year: str = Field(index=True)
  category: str = Field(index=True)
