from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query

from ..dependencies import SessionDep
from ..models.misc import ResponseWrapper
from ..models.user import UserInfoRegister
from ..services.user import create_user, read_user
from ..utils.authentification import user_to_token

router = APIRouter(
  prefix='/user',
  tags=['user'],
  responses={404: {'description': 'Not found'}}
)


@router.post('/register')
async def register(
        user: Annotated[UserInfoRegister, Body()],
        session: SessionDep
) -> ResponseWrapper:
  if create_user(user, session):
    return ResponseWrapper(data=None)
  return ResponseWrapper(status=1, data=None)


@router.post('/login')
async def login(
        email: Annotated[str, Body()],
        password: Annotated[str, Body()],
        session: SessionDep
) -> ResponseWrapper[dict]:
  user = read_user(email, password, session)
  if user is None:
    return ResponseWrapper(status=1, data={})
  data = {
    'username': user.username,
    'premium': user.premium,
    'token': user_to_token(user)
  }
  return ResponseWrapper(data=data)
