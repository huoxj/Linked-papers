from sqlmodel import Session, select

from app.models.user import User, UserRegister
from app.schemas.user import UserInDB
from app.utils.encryption import encrypt_string, verify_string, hash_string


def create_user(
        user: UserRegister,
        session: Session
) -> bool:
  user_in_db = UserInDB(
    username=user.username,
    premium=user.premium,
    encrypted_email=encrypt_string(user.email),
    encrypted_password=encrypt_string(user.password),
    email_hash=hash_string(user.email)
  )
  session.add(user_in_db)
  session.commit()
  session.refresh(user_in_db)
  return True


def read_user(
        email: str,
        session: Session
) -> UserRegister | None:
  user = (session.exec(select(UserInDB)
                       .where(hash_string(email) == UserInDB.email_hash))
          .first())
  if user is None:
    return None
  return UserRegister(id=user.id, email=email, username=user.username,
                      premium=user.premium, password=user.encrypted_password)
