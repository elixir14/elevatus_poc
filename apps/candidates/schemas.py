from pydantic import BaseModel, Field, EmailStr

from apps.candidates.constants import Gender
from elevatus_poc.core.schemas import ResponseBaseModel


class CandidateSchema(ResponseBaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)
    user_id: str
    career_level: str = Field(...)
    job_major: str = Field(...)
    years_of_experience: int = Field(...)
    degree_type: str = Field(...)
    skills: list = Field(...)
    nationality: str = Field(...)
    city: str = Field(...)
    salary: str = Field(...)
    gender: Gender = Gender.MALE.value


class CandidateCreateSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)
    career_level: str = Field(...)
    job_major: str = Field(...)
    years_of_experience: int = Field(...)
    degree_type: str = Field(...)
    skills: list = Field(...)
    nationality: str = Field(...)
    city: str = Field(...)
    salary: str = Field(...)
    gender: Gender = Gender.MALE.value

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "smith",
                "email": "jon@usa.com",
                "career_level": "Senior",
                "job_major": "Computer Science",
                "years_of_experience": 5,
                "degree_type": "Master",
                "skills": ["Python", "Mongodb"],
                "nationality": "xxxx",
                "city": "xxxx",
                "salary": "xxxx",
                "gender": Gender.MALE.value,
            }
        }


class CandidateUpdateSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    career_level: str = Field(...)
    job_major: str = Field(...)
    years_of_experience: int = Field(...)
    degree_type: str = Field(...)
    skills: list = Field(...)
    nationality: str = Field(...)
    city: str = Field(...)
    salary: str = Field(...)
    gender: Gender = Gender.MALE.value

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "smith",
                "career_level": "Senior",
                "job_major": "Computer Science",
                "years_of_experience": 5,
                "degree_type": "Master",
                "skills": ["Python", "Mongodb"],
                "nationality": "xxxx",
                "city": "xxxx",
                "salary": "xxxx",
                "gender": Gender.MALE.value,
            }
        }
