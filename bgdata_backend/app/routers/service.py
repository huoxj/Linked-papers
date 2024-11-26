from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends

from ..models.misc import ResponseWrapper
from ..models.user import UserInfo
from ..dependencies import get_current_user

router = APIRouter(
  prefix='/service',
  tags=['service'],
  responses={404: {'description': 'Not found'}}
)


@router.get('/search')
async def search(
        key: Annotated[str, Query()],
        page: Annotated[int, Query(ge=1)],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/recommend')
async def recommend(
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper:
  raise HTTPException(status_code=500, detail='Unimplemented.')
