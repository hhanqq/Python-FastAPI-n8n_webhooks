from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserCreate):
    pass

class UserPublic(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserAddRole(UserBase):
    id: int
    username: str