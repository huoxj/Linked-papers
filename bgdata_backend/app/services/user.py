from sqlmodel import Session, select

from app.models.user import UserInfo, UserInfoRegister
from app.schemas.user import User
from app.utils.encryption import encrypt_password


def create_user(
        user: UserInfoRegister,
        session: Session
) -> bool:
  user_in_db = User(
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
) -> UserInfo:
  encrypted_password = encrypt_password(password)
  return (session.exec(select(User)
                       .where(User.email == email and User.encrypted_password == encrypted_password))
          .first())
