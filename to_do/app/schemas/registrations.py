from pydantic import BaseModel, Field, EmailStr

class SRegister(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)