from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., description="Registered email to access platform")
    password: str = Field(..., description="Registered password to access platform")


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int = Field(..., description="User Id")
    created_time: datetime = Field(..., description="Time of user creation")
    modified_time: datetime = Field(..., description="Time of user update")

    class Config:
        orm_mode = True
