from pydantic import BaseModel, Field
from typing import Optional


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class PetSchema(BaseModel):
    id: int
    name: str
    category: Optional[Category] = None
    photoUrls: list[str] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)
    status: str = Field(default="available", pattern=r"^(available|pending|sold)$")
