from pydantic import BaseModel, Field, ConfigDict


class STaskBase(BaseModel):
    task_name: str = Field(...)
    task_description: str = Field(default='')

class STaskAdd(STaskBase):
    pass

class STaskUpd(BaseModel):
    task_name: str
    task_description: str
    is_checked: bool

class STaskShow(STaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_checked: bool