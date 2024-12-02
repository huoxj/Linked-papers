import yaml
from fastapi import HTTPException, status

from app.models.user import User
from app.utils.search_engine import search


def search_with_key(
        key: str,
        page: int
) -> dict:
  ids = search(key)
  with open('config/config.yaml', 'r') as f:
    page_size = yaml.safe_load(f)['search']['page_size']
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
