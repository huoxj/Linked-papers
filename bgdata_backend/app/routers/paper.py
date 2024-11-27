from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from ..dependencies import get_current_user
from ..models.misc import ResponseWrapper
from ..models.user import UserInfo

router = APIRouter(
  prefix='/paper',
  tags=['paper'],
  responses={404: {'description': 'Not found'}}
)


@router.get('/abstract')
async def get_abstract(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[str]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/title')
async def get_title(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[str]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/reference')
async def get_reference_list(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[list[int]]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/year')
async def get_year(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[str]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/category')
async def get_category(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[str]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/related')
async def get_related_list(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[list[int]]:
  raise HTTPException(status_code=500, detail='Unimplemented.')


@router.get('/samecategory')
async def get_same_category_list(
        paper_id: Annotated[int, Query(alias='id')],
        user: Annotated[UserInfo, Depends(get_current_user)]
) -> ResponseWrapper[list[int]]:
  raise HTTPException(status_code=500, detail='Unimplemented.')
