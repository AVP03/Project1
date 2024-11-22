# schemas/payment.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    order_id: int
    card_information: str
    transaction_status: str
    payment_type: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int
    created_at: datetime
    
class PaymentResponse(BaseModel):
    payment_id: int
    order_id: int
    transaction_status: str
    payment_type: str
    created_at: datetime
    customer_name: Optional[str] = None

    class Config:
        orm_mode = True
