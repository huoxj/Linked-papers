from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..models.misc import ResponseWrapper
from ..models.user import UserInfoIn


router = APIRouter(
  prefix='/user',
  tags=['user'],
  responses={404: {'description': 'Not found'}}
)


@router.post('/register')
async def register(
        user: Annotated[UserInfoIn, Query()]
) -> ResponseWrapper:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.post('/login')
async def login(
        email: Annotated[str, Query()],
        password: Annotated[str, Query()]
) -> ResponseWrapper:
  raise HTTPException(status_code=500, detail='Unimplemented.')
