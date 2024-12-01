from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    guest: Optional[bool] = False

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class Customer(CustomerBase):
    customer_id: int

    class Config:
        orm_mode = True
