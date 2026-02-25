from pydantic import BaseModel, Field

class SUserRegister(BaseModel):
        email: str = Field(...)
        password: str = Field(...)
        phone_number: str = Field(...)
        first_name: str = Field(...)
        last_name: str = Field(...)

class SUserAuth(BaseModel):
        email: str = Field(...)
        password: str = Field(...)

        