# controllers/customer.py
from sqlalchemy.orm import Session
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate
from fastapi import HTTPException, status
from ..models.orders import Order

#create customer - ani
def create(db: Session, customer_data: CustomerCreate):
    db_customer = Customer(**customer_data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

#read one customer - ani
def read_one(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

def read_all(db: Session):
    return db.query(Customer).all()

def update(db: Session, customer_id: int, customer_data: CustomerCreate):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer:
        db_customer.name = customer_data.name
        db_customer.email = customer_data.email
        db_customer.phone_number = customer_data.phone_number
        db_customer.address = customer_data.address
        db_customer.guest = customer_data.guest

        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None

def delete(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    #check if the customer has orders
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    if orders:
        raise HTTPException(status_code=400, detail="Cannot delete customer with existing orders.")
    
    db.delete(customer)
    db.commit()
    
    return {"message": "Customer deleted successfully."}
