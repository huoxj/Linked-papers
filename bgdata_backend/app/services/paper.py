from sqlmodel import Session, select

from app.models.paper import Paper
from app.schemas.paper import PaperInDB


def read_paper(paper_id: int, session: Session) -> Paper:
  return (session.exec(select(PaperInDB)
                       .where(PaperInDB.id == paper_id))
          .first())


def read_related_papers(paper_id: int, session: Session) -> list[int]:
  # TODO
  return []


def read_papers_with_same_category(paper_id: int, session: Session) -> list[int]:
  paper = read_paper(paper_id, session)
  papers = (session.exec(select(PaperInDB)
                         .where(PaperInDB.category == paper.category))
            .all())
  return [paper.id for paper in papers]
