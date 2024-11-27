from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(String(500), nullable=True)  # Text review, nullable
    rating = Column(Integer, nullable=False)  # Numeric rating (1-5)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="ratings")
    customer = relationship("Customer", back_populates="ratings")