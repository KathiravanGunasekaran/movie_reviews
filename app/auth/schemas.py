from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class TokenDetails(BaseModel):
    token_type: str
    token: str


class TokenData(BaseModel):
    id: int | None
