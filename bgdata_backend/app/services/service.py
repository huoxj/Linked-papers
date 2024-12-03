import re
from datetime import datetime

import yaml
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.paper import PaperInDB
from app.utils.search_engine import search_by_similarity, calc_matching_score, calc_similarity_score, \
  calc_up_to_date_score, calc_citation_score

with open('config/config.yaml', 'r') as f:
  search_config = yaml.safe_load(f)['search']


def search_with_full_text(
        keywords_str: str,
        session: Session
) -> list[PaperInDB]:
  result = session.exec(select(PaperInDB)
                        .where(text('MATCH (title, abstract) AGAINST (:keywords IN NATURAL LANGUAGE MODE)')
                               .params(keywords=keywords_str))
                        .limit(search_config['max_results'])).all()
  return list(result)


def search_with_similarity(
        keywords: list[str],
        session: Session
) -> list[int]:
  ids_by_similarity = search_by_similarity(keywords)
  return [
    session.exec(select(PaperInDB)
                 .where(PaperInDB.id == paper_id))
    .first()
    for paper_id in ids_by_similarity]


def search_with_key(
        key: str,
        page: int,
        session: Session
) -> dict:
  keywords = re.sub(r'[^\w\s]', '', key.lower()).split()

  results_matching = search_with_full_text(' '.join(keywords), session)
  results_similarity = search_with_similarity(keywords, session)
  candidates = []
  candidates.extend(results_matching)
  candidates.extend(results_similarity)

  current_year = datetime.now().year
  scores = []
  for candidate in candidates:
    matching_index = -1 if candidate not in results_matching else results_matching.index(candidate)
    similarity_index = -1 if candidate not in results_similarity else results_similarity.index(candidate)
    scores.append(
      search_config['weight_matching'] * calc_matching_score(matching_index)
      + search_config['weight_similarity'] * calc_similarity_score(similarity_index)
      + search_config['weight_up_to_date'] * calc_up_to_date_score(int(candidate.year) - current_year)
      + search_config['weight_citation'] * calc_citation_score(candidate.citation_count)
    )
  ids = [candidate[0].id for candidate in sorted(zip(candidates, scores),
                                                 key=lambda x: x[1], reverse=True)][:search_config['max_results']]

  page_size = search_config['page_size']
  num_page = (len(ids) + page_size - 1) // page_size
  if page > num_page:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Page out of range.')
  return {
    'idList': ids[(page - 1) * page_size: page * page_size],
    'totalPage': num_page
  }


def recommend_for_user(
        user: User
) -> list[int]:
  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail='Unimplemented.')
