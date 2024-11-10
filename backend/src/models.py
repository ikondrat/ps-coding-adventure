# models.py
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(alias='full_name')  
    email: int

Base = declarative_base()

