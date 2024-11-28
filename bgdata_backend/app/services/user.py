from sqlmodel import Session, select

from app.models.user import User, UserRegister
from app.schemas.user import UserInDB
from app.utils.encryption import encrypt_password


def create_user(
        user: UserRegister,
        session: Session
) -> bool:
  user_in_db = UserInDB(
    email=user.email,
    username=user.username,
    premium=user.premium,
    encrypted_password=encrypt_password(user.password)
  )
  session.add(user_in_db)
  session.commit()
  session.refresh(user_in_db)
  return True


def read_user(
        email: str,
        password: str,
        session: Session
) -> User:
  encrypted_password = encrypt_password(password)
  return (session.exec(select(UserInDB)
                       .where(UserInDB.email == email and UserInDB.encrypted_password == encrypted_password))
          .first())
