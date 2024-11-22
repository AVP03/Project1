from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import customer as controller
from ..schemas.customer import CustomerCreate, CustomerResponse
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# CREATE a customer
@router.post("/", response_model=CustomerResponse)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, customer_data=customer_data)

# READ a customer by ID
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, customer_id=customer_id)

# READ all customers
@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

# UPDATE a customer by ID
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_data: CustomerCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, customer_id=customer_id, customer_data=customer_data)

# DELETE a customer by ID
@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, customer_id=customer_id)
