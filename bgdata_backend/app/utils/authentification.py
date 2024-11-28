from fastapi.security import OAuth2PasswordBearer

from app.models.user import User


def user_to_token(user: User) -> str:
  # TODO
  return 'fake_token'


def token_to_user(token: str) -> User:
  # TODO
  return User(username='fake_user', email='fake@email.com', premium=False)
