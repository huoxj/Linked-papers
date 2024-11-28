from typing import Annotated

from fastapi.params import Depends, Header
from sqlmodel import Session

from app.models.user import User
from app.utils.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]


def authenticate_user(token: Annotated[str, Header(alias='token')]):
  pass


def get_current_user():
  # if not current_user, raises an exception to indicate unauthorized
  # otherwise, returns an UserInfo
  pass


def require_premium(user: Annotated[User, Depends(get_current_user)]):
  pass
