from pydantic import BaseModel


class Role(BaseModel):
    id: int
    role: str


class User(BaseModel):
    id: int
    email: str
    username: str
    password: str
    name: str
    surname: str
    # role_id: int
    role_id: Role


class UserIn(BaseModel):
    email: str
    username: str
    password: str
    name: str
    surname: str
    role_id: int
