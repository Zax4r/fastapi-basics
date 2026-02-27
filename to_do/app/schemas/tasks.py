from pydantic import BaseModel, Field


class STaskBase(BaseModel):
    task_name: str = Field(...)
    task_description: str = Field(default='')

class STaskAdd(STaskBase):
    pass

class STaskShow(STaskBase):
    id: int