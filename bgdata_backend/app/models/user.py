from pydantic import BaseModel


class UserInfo(BaseModel):
    email: str
    username: str
    premium: bool


class UserInfoIn(UserInfo):
    password: str


class UserInfoInDB(UserInfo):
    encrypted_password: str
