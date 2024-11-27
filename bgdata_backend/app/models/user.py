from pydantic import BaseModel


class UserInfo(BaseModel):
    email: str
    username: str
    premium: bool


class UserInfoRegister(UserInfo):
    password: str
