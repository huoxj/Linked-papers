from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  email: str = Field(index=True)
  username: str = Field(index=True)
  premium: bool = Field(index=True)
  encrypted_password: str = Field()
