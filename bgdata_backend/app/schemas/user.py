from sqlmodel import SQLModel, Field


class UserInDB(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  username: str = Field(index=True)
  premium: bool = Field(index=True)
  encrypted_email: str = Field()
  encrypted_password: str = Field()

  email_hash: str = Field(index=True)
