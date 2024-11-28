from typing import Annotated

from fastapi import APIRouter, Body

from ..dependencies import SessionDep
from ..models.misc import ResponseWrapper
from ..models.user import UserRegister
from ..services.user import create_user, read_user
from ..utils.authentification import user_to_token
from ..utils.encryption import verify_string

router = APIRouter(
  prefix='/user',
  tags=['user'],
  responses={404: {'description': 'Not found'}}
)


@router.post('/register')
async def register(
        user: Annotated[UserRegister, Body()],
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
  user = read_user(email, session)
  if user is None or not verify_string(password, user.password):
    return ResponseWrapper(status=1, data={})
  data = {
    'username': user.username,
    'premium': user.premium,
    'token': user_to_token(user)
  }
  return ResponseWrapper(data=data)
