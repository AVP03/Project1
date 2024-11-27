from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    item: str
    amount: int
    unit: str


class ResourceCreate(ResourceBase):
    item: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[str] = None


class ResourceUpdate(BaseModel):
    item: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[str] = None


class Resource(ResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True
