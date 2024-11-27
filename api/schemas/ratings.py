from pydantic import BaseModel
from datetime import datetime

class RatingCreate(BaseModel):
    review_text: str
    rating: int
    order_id: int
    customer_id: int

    class Config:
        orm_mode = True


class RatingResponse(BaseModel):
    id: int
    review_text: str
    rating: int
    order_id: int
    customer_id: int

    class Config:
        orm_mode = True
