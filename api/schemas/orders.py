from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    customer_name: str
    description: Optional[str]
    customer_id: int = None
    
    class ConfigDict:
        from_attributes = True

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    
class OrderResponse(BaseModel):
    id: int
    customer_name: str
    order_date: Optional[datetime] = None
    description: Optional[str] = None
    order_details: List[OrderDetail]  # Assuming you have the OrderDetail schema defined


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
