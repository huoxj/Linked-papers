from sqlmodel import SQLModel, Field, Relationship


class PaperReferenceLink(SQLModel, table=True):
  source_id: int = Field(foreign_key='paperindb.id', primary_key=True)
  target_id: int = Field(foreign_key='paperindb.id', primary_key=True)


class PaperInDB(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  abstract: str = Field(index=True)
  title: str = Field(index=True)
  year: str = Field(index=True)
  category: str = Field(index=True)

  references: list['PaperInDB'] = Relationship(
    back_populates='referenced_by',
    link_model=PaperReferenceLink,
    sa_relationship_kwargs={'primaryjoin': 'PaperInDB.id == PaperReferenceLink.source_id',
                            'secondaryjoin': 'PaperInDB.id == PaperReferenceLink.target_id'}
  )
  referenced_by: list['PaperInDB'] = Relationship(
    back_populates='references',
    link_model=PaperReferenceLink,
    sa_relationship_kwargs={'primaryjoin': 'PaperInDB.id == PaperReferenceLink.target_id',
                            'secondaryjoin': 'PaperInDB.id == PaperReferenceLink.source_id'}
  )


class SimilarityInDB(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  source_id: int = Field(index=True)
  target_id: int = Field(index=True)
  similarity: float = Field(index=True)
