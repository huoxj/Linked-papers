from typing import Annotated

import yaml
from fastapi.params import Depends, Header
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from app.models.user import User

with open('config/config.yaml') as f:
  mysql_config = yaml.safe_load(f)['mysql']

db_engine = create_engine(
  f'mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['url']}:{mysql_config['port']}/{mysql_config['database']}',
  echo=True
)


def create_db_and_tables():
  SQLModel.metadata.create_all(db_engine)


def get_session():
  with Session(db_engine) as session:
    yield session


SessionDep = Annotated[Session, Depends(get_session)]


def verify_token(token: Annotated[str, Header(alias='token')]):
  pass


def get_current_user():
  # if not current_user, raises an exception to indicate unauthorized
  # otherwise, returns an UserInfo
  pass


def verify_premium(user: Annotated[User, Depends(get_current_user)]):
  pass
