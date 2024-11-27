from fastapi.security import OAuth2PasswordBearer

from app.models.user import UserInfo


def user_to_token(user: UserInfo) -> str:
  return 'fake_token'


def token_to_user(token: str) -> UserInfo:
  return UserInfo(username='fake_user', email='fake@email.com', premium=False)
