import datetime
from pydantic import BaseModel, ValidationError, validator


class RegisterData(BaseModel):
    phone: str
    nickname: str
    password: str
    first_name: str
    last_name: str
    birth_date: datetime.date

    @validator('nickname')
    def nickname_has_spaces(cls, v):
        if ' ' in v:
            raise ValueError('Nickname must not contain a space')

        return v.title()

    @validator('birth_date')
    def age_must_be_at_least_sixteen(cls, v):
        today = datetime.date.today()

        if (today.year - v.year) < 16:
            raise ValueError('Your age must be at least 16')
        return v

