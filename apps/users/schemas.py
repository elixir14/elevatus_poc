from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


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
