from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends

from ..models.user import User
from ..dependencies import get_current_user, authenticate_user, ResponseWrapper
from ..services.service import search_with_key, recommend_for_user

router = APIRouter(
  prefix='/service',
  tags=['service'],
  responses={404: {'description': 'Not found'}}
)


@router.get('/search', dependencies=[Depends(authenticate_user)])
async def search(
        key: Annotated[str, Query()],
        page: Annotated[int, Query(ge=1)],
) -> ResponseWrapper[dict]:
  result = search_with_key(key, page)
  return ResponseWrapper(data=result)


@router.get('/recommend', dependencies=[Depends(authenticate_user)])
async def recommend(
        user: Annotated[User, Depends(get_current_user)]
) -> ResponseWrapper[list[int]]:
  result = recommend_for_user(user)
  return ResponseWrapper(data=result)
