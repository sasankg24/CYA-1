from pydantic import BaseModel, Field
from typing import Optional


class DogCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age_years: Optional[int] = Field(default=None, ge=0)
    breed: Optional[str] = Field(default=None, max_length=100)
    color: Optional[str] = Field(default=None, max_length=50)


class DogUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    age_years: Optional[int] = Field(default=None, ge=0)
    breed: Optional[str] = Field(default=None, max_length=100)
    color: Optional[str] = Field(default=None, max_length=50)


class DogOut(BaseModel):
    id: str
    name: str
    age_years: Optional[int] = None
    breed: Optional[str] = None
    color: Optional[str] = None