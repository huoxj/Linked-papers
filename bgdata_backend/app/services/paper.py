from sqlmodel import Session, select

from app.models.paper import Paper
from app.schemas.paper import PaperInDB, SimilarityInDB


def read_paper(
        paper_id: int,
        session: Session
) -> PaperInDB | None:
  return (session.exec(select(PaperInDB)
                       .where(PaperInDB.id == paper_id))
          .first())


def read_related_papers(
        paper_id: int,
        session: Session
) -> list[int]:
  rows = (session.exec(select(SimilarityInDB)
               .where(SimilarityInDB.source_id == paper_id)).all())
  # dicts = [{'id': row.target_id, 'similarity': row.similarity} for row in rows]
  # dicts.sort(key=lambda x: x[1], reverse=True)
  # return dicts
  ids = [row.target_id for row in rows]
  ids.sort(reverse=True)
  return ids


def read_papers_with_same_category(paper_id: int, session: Session) -> list[int]:
  paper = read_paper(paper_id, session)
  papers = (session.exec(select(PaperInDB)
                         .where(PaperInDB.category == paper.category)
                         .limit(10))
            .all())
  return [paper.id for paper in papers]
