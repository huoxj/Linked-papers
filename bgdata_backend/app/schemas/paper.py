from sqlmodel import SQLModel, Field, Relationship


class PaperInDB(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  abstract: str = Field(index=True)
  title: str = Field(index=True)
  year: str = Field(index=True)
  category: str = Field(index=True)

  references: list['PaperInDB'] = Relationship(
    back_populates='referenced_by',
  )
  referenced_by: list['PaperInDB'] = Relationship(
    back_populates='references',
    sa_relationship_kwargs={'remote_side': 'PaperInDB.id'}
  )
  reference_id: int | None = Field(default=None, foreign_key='paperindb.id')


class SimilarityInDB(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  source_id: int = Field(index=True)
  target_id: int = Field(index=True)
  similarity: float = Field(index=True)
