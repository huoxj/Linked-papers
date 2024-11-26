from pydantic import BaseModel


class ResponseWrapper(BaseModel):
  status: int
  data: dict
