from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    username: str
    premium: bool


class UserRegister(User):
    password: str
