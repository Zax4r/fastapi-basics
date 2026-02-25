from pydantic import BaseModel, Field, ConfigDict

class SMajor(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    major_name: str = Field(...)
    major_description: str = Field(...)
    students_count: int = Field(0)


class SMajorAdd(BaseModel):
    major_name: str = Field(...)
    major_description: str = Field(...)
    students_count: int = Field(0)

class SMajorUpdDesc(BaseModel):
    major_name: str = Field(...)
    major_description: str = Field(None)
