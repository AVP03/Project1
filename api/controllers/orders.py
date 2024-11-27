from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import orders as order_model, customer as customer_model
from ..schemas.orders import OrderCreate
from datetime import datetime
from ..schemas.orders import OrderResponse

from uuid import uuid4

def create(db: Session, request):
    # Check if the customer_id exists in the request
    customer_id = request.customer_id

    # If no customer_id, create a guest customer with the provided name or default to "Guest"
    if not customer_id:
        guest_customer = customer_model.Customer(
            name=request.customer_name if request.customer_name else "Guest",  # Use provided name or "Guest"
            email=f"guest_{uuid4().hex}@example.com",  # Generate unique email
            phone_number=None,
            address=None,
            guest=True  # Mark this as a guest customer
        )
        db.add(guest_customer)
        db.commit()
        db.refresh(guest_customer)
        customer_id = guest_customer.customer_id

    # Create the order linked to the customer (regular or guest)
    new_order = order_model.Order(
        customer_id=customer_id,
        description=request.description
    )
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order




def create_order_with_customer(db: Session, request: OrderCreate):
    """
    Create a new order. If the customer does not exist, create a new customer.
    """
    # Check if the customer exists
    db_customer = db.query(customer_model.Customer).filter(
        customer_model.Customer.customer_id == request.customer_id
    ).first()

    if not db_customer:
        # Create a new customer
        db_customer = customer_model.Customer(
            name=request.customer_name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

    # Create the order
    new_order = order_model.Order(
        customer_id=db_customer.customer_id,
        description=request.description,
        order_date=datetime.utcnow()  # Fixed datetime issue here
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order


def read_all(db: Session):
    """
    Retrieve all orders, including customer information and order details.
    """
    try:
        # Join Order with Customer based on customer_id
        result = db.query(order_model.Order, customer_model.Customer).join(
            customer_model.Customer, order_model.Order.customer_id == customer_model.Customer.customer_id
        ).all()

        # Prepare the response
        orders = [
            OrderResponse(
                id=order.id,
                customer_name=customer.name,  # Get customer_name from the Customer model
                customer_id=customer.customer_id,  # customer_id from Customer model
                description=order.description,
                order_date=order.order_date,
                order_details=order.order_details if order.order_details else []  # Ensure order_details is not None
            ) 
            for order, customer in result  # Unpacking the result of the join
        ]
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return orders




def read_one(db: Session, item_id: int):
    """
    Retrieve a specific order by its ID, including customer information.
    """
    try:
        item = db.query(order_model.Order, customer_model.Customer).join(
            customer_model.Customer, order_model.Order.customer_id == customer_model.Customer.customer_id
        ).filter(order_model.Order.id == item_id).first()

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id: int, request: OrderCreate):
    """
    Update an existing order by its ID.
    """
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id: int):
    """
    Delete an order by its ID.
    """
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
