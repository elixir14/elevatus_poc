from enum import Enum


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIC = "Not Specific"
