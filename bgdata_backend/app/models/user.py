from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str
    premium: bool


class UserRegister(User):
    password: str
