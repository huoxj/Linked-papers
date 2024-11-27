from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query

from ..models.misc import ResponseWrapper
from ..models.user import UserInfoRegister


router = APIRouter(
  prefix='/user',
  tags=['user'],
  responses={404: {'description': 'Not found'}}
)


@router.post('/register')
async def register(
        user: Annotated[UserInfoRegister, Body()]
) -> ResponseWrapper[dict]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.post('/login')
async def login(
        email: Annotated[str, Body()],
        password: Annotated[str, Body()],
) -> ResponseWrapper[dict]:
  raise HTTPException(status_code=500, detail='Unimplemented.')
