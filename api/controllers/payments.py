
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.payments import Payment
from ..schemas.payments import PaymentCreate
from ..models.orders import Order
from ..models.customer import Customer

def get_all_payments(db: Session):
    #get all payments and join with orders and customers to get customer names
    payments = db.query(Payment).all()  

    #for each payment, get the customer name by joining with the order and customer tables
    for payment in payments:
        order = db.query(Order).join(Customer).filter(Order.id == payment.order_id).first()
        if order:
            payment.customer_name = order.customer.name  
        else:
            payment.customer_name = None  
    
    return payments



def create_payment(db: Session, payment_data: PaymentCreate):
    new_payment = Payment(**payment_data.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

def get_payment_by_order_id(db: Session, order_id: int):
    payment = db.query(Payment).filter(Payment.order_id == order_id).first()
    
    
    if payment:
        order = db.query(Order).join(Customer).filter(Order.id == order_id).first()
        if order:
            
            order.customer_name = order.customer.name
    
    return payment


def update_payment(db: Session, payment_id: int, payment_data: PaymentCreate):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    for key, value in payment_data.dict().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment

def delete_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}
