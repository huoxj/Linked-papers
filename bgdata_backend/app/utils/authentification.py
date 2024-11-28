from datetime import datetime, timedelta, timezone

import jwt
import yaml
from jwt import InvalidTokenError
from sqlmodel import Session

from app.models.user import User
from app.services.user import read_user

with open('config/config.yaml') as f:
  auth_config = yaml.safe_load(f)['auth']


def user_to_token(user: User) -> str:
  to_encode = {
    'email': user.email,
    'expiration': (datetime.now(timezone.utc) + timedelta(minutes=auth_config['expired_time'])).timestamp()
  }
  return jwt.encode(to_encode, auth_config['secret_key'], algorithm=auth_config['algorithm'])


def token_to_user(token: str, session: Session) -> User | None:
  try:
    payload = jwt.decode(token, auth_config['secret_key'], algorithms=[auth_config['algorithm']])
    email = payload.get('email')
  except InvalidTokenError:
    return None
  if datetime.fromtimestamp(payload.get('expiration'), timezone.utc) < datetime.now(timezone.utc):
    return None
  return read_user(email, session)
