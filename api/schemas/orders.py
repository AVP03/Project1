from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderDetailCreate(BaseModel):
    sandwich_id: int
    quantity: int  

    class Config:
        orm_mode = True
        
class OrderDetailResponse(BaseModel):
    id: int
    order_id: int
    sandwich_id: int
    sandwich_name: str
    quantity: int
    price: float
    amount: int

class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(BaseModel):
    customer_id: int = None
    customer_name: str = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str]
    order_details: List[OrderDetailCreate]
    
    class ConfigDict:
        from_attributes = True

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    
class OrderResponse(BaseModel):
    id: int
    customer_id: int
    customer_name: str
    description: Optional[str]
    total_price: float
    order_details: List[OrderDetail]  


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
