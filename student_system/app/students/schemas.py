from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import date, datetime
from typing import Optional
import re


class SStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    phone_number: str = Field(default=...)
    first_name: str = Field(default=..., min_length=1, max_length=50)
    last_name: str = Field(default=..., min_length=1, max_length=50)
    date_of_birth: date = Field(default=...)
    email: EmailStr = Field(default=...)
    address: str = Field(default=..., min_length=10, max_length=200)
    enrollment_year: int = Field(default=..., ge=2002)
    major_id: int = Field(default=..., ge=1)
    course: int = Field(default=..., ge=1, le=5)
    special_notes: Optional[str] = Field(default=None, max_length=500)
    photo: Optional[str] = Field(default=None)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+[\d\s\-\(\)]{7,20}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return values

class SStudentAdd(SStudent):
    pass

class SStudentUpdAddr(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...)
    address: str = Field(..., min_length=10, max_length=200)


    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+[\d\s\-\(\)]{7,20}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values
