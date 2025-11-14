from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True