from fastapi import HTTPException

from app.models.user import User


def search_with_key(key: str, page: int) -> dict:
  # TODO
  raise HTTPException(status_code=500, detail='Unimplemented.')


def recommend_for_user(user: User) -> list[int]:
  # TODO
  raise HTTPException(status_code=500, detail='Unimplemented.')
