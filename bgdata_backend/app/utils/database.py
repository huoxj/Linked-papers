import yaml
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

with open('config/config.yaml') as f:
  mysql_config = yaml.safe_load(f)['mysql']

db_engine = create_engine(
  f'mysql+pymysql://{mysql_config["user"]}:{mysql_config["password"]}'
  f'@{mysql_config["url"]}:{mysql_config["port"]}/{mysql_config["database"]}',
  echo=True
)


def create_db_and_tables():
  SQLModel.metadata.create_all(db_engine)


def get_session():
  with Session(db_engine) as session:
    yield session
