from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from ..dependencies import get_current_user, get_session, verify_token, verify_premium
from ..models.misc import ResponseWrapper
from ..services.paper import read_paper, read_related_papers, read_papers_with_same_category

router = APIRouter(
  prefix='/paper',
  tags=['paper'],
  responses={404: {'description': 'Not found'}}
)


@router.get('/abstract', dependencies=[Depends(verify_token)])
async def get_abstract(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[str]:
  paper = read_paper(paper_id, session)
  if paper is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=paper.abstract)


@router.get('/title', dependencies=[Depends(verify_token)])
async def get_title(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[str]:
  paper = read_paper(paper_id, session)
  if paper is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=paper.title)


@router.get('/reference', dependencies=[Depends(verify_token)])
async def get_reference_list(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[list[int]]:
  paper = read_paper(paper_id, session)
  if paper is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=paper.references)


@router.get('/year', dependencies=[Depends(verify_token)])
async def get_year(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[str]:
  paper = read_paper(paper_id, session)
  if paper is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=paper.year)


@router.get('/category', dependencies=[Depends(verify_token)])
async def get_category(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[str]:
  paper = read_paper(paper_id, session)
  if paper is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=paper.category)


@router.get('/related', dependencies=[Depends(verify_token), Depends(verify_premium)])
async def get_related_list(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[list[int]]:
  papers = read_related_papers(paper_id, session)
  if papers is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=papers)


@router.get('/samecategory', dependencies=[Depends(verify_token), Depends(verify_premium)])
async def get_same_category_list(
        paper_id: Annotated[int, Query(alias='id')],
        session: Annotated[Session, Depends(get_session)]
) -> ResponseWrapper[list[int]]:
  papers = read_papers_with_same_category(paper_id, session)
  if papers is None:
    return ResponseWrapper(status=1, data=None)
  return ResponseWrapper(data=papers)
