import hashlib

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def encrypt_string(password: str) -> str:
  return pwd_context.hash(password)


def verify_string(password: str, hashed_password: str) -> bool:
  return pwd_context.verify(password, hashed_password)


def hash_string(string: str) -> str:
  return hashlib.sha256(string.encode('utf-8')).hexdigest()
