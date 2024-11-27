from pydantic import BaseModel
from typing_extensions import TypeVar, Generic

T = TypeVar('T')


class ResponseWrapper(BaseModel, Generic[T]):
  status: int
  data: T
