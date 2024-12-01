from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)  
    phone_number = Column(String(15), nullable=True) 
    address = Column(String(200), nullable=True) 
    guest = Column(Boolean, default=False)

    #Relationships
    orders = relationship("Order", back_populates="customer")
    ratings = relationship("Rating", back_populates="customer")
