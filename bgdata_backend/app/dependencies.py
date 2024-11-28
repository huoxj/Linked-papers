from typing import Annotated

from fastapi import HTTPException, status
from fastapi.params import Depends, Header
from sqlmodel import Session

from app.models.user import User
from app.utils.authentification import token_to_user
from app.utils.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]


def authenticate_user(
        token: Annotated[str, Header(alias='token')],
        session: SessionDep
) -> User:
  user = token_to_user(token, session)
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Invalid token.'
    )
  return user


def get_current_user(
        user: Annotated[User, Depends(authenticate_user)]
) -> User:
  """
  Returns the current user.
  This function is an alias for authenticate_user.
  """
  return user


def require_premium(
        user: Annotated[User, Depends(get_current_user)]
) -> None:
  if not user.premium:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='Not a premium user.'
    )
