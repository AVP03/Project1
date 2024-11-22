# routers/payment.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import payments as controller
from ..schemas.payments import PaymentCreate, Payment, PaymentResponse
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

@router.post("/", response_model=Payment)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    return controller.create_payment(db=db, payment_data=payment_data)

@router.get("/{order_id}", response_model=Payment)
def get_payment(order_id: int, db: Session = Depends(get_db)):
    return controller.get_payment_by_order_id(db=db, order_id=order_id)

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment_data: PaymentCreate, db: Session = Depends(get_db)):
    return controller.update_payment(db=db, payment_id=payment_id, payment_data=payment_data)

@router.delete("/{payment_id}", response_model=dict)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return controller.delete_payment(db=db, payment_id=payment_id)

@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return controller.get_all_payments(db=db)
