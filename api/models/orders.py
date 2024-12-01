from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="SET NULL"), nullable=True)
    order_date = Column(DateTime, nullable=False, server_default=func.now())
    description = Column(String(300))
    total_price = Column(Float, nullable=True, default=0.0)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)
    ratings = relationship("Rating", back_populates="order")
