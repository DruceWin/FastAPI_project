from pydantic import BaseModel


class Role(BaseModel):
    id: int
    role: str


class User(BaseModel):
    id: int
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    role_id: int
    # role_id: Role


class UserIn(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    role_id: int


class UserPatch(BaseModel):
    email: str = None
    username: str = None
    password: str = None
    first_name: str = None
    second_name: str = None
    role_id: int = None


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    refresh: str
