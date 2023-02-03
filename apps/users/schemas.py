from pydantic import BaseModel, Field, EmailStr

from elevatus_poc.core.schemas import ResponseBaseModel


class UserSchema(ResponseBaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)


class UserCreateSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "smith",
                "email": "jon@usa.com",
                "password": "xxxx",
            }
        }


class UserUpdateSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "smith",
            }
        }


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenBase(BaseModel):
    access: str
    refresh: str
