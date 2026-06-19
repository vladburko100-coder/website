from pydantic import BaseModel, Field


class Users(BaseModel):
    name: str = Field(...)
    fullname: str = Field(...)
    phone: str = Field(...)
