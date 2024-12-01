from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import orders as order_model, customer as customer_model
from ..models import sandwiches
from ..models import recipes
from ..models import resources
from ..models import order_details
from ..schemas.orders import OrderCreate
from datetime import datetime
from ..schemas.orders import OrderResponse
from decimal import Decimal
from uuid import uuid4
from decimal import Decimal


def create(db: Session, request: OrderCreate):
    # Validate or fetch customer
    customer = None

    if request.customer_id:
        # If customer_id is provided, fetch the customer
        customer = db.query(customer_model.Customer).filter(
            customer_model.Customer.customer_id == request.customer_id
        ).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
    else:
        # If no customer_id, create a guest customer
        if not request.customer_name or not request.email:
            raise HTTPException(
                status_code=400,
                detail="Customer name and email are required to create a new customer."
            )
        customer = customer_model.Customer(
            name=request.customer_name,
            email=f"guest_{uuid4().hex}@example.com",  
            phone_number=request.phone_number,
            address=request.address,
            guest=True  
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # Create the order
    new_order = order_model.Order(
        customer_id=customer.customer_id,
        description=request.description,
        order_date=datetime.utcnow()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total_price = Decimal(0)  
    order_details_response = []  

    # Process each sandwich in the order
    for detail in request.order_details:
        sandwich = db.query(sandwiches.Sandwich).filter(
            sandwiches.Sandwich.id == detail.sandwich_id
        ).first()
        if not sandwich:
            raise HTTPException(status_code=404, detail=f"Sandwich with ID {detail.sandwich_id} not found")

        # Deduct resources and validate availability
        recipes_for_sandwich = db.query(recipes.Recipe).filter(
            recipes.Recipe.sandwich_id == sandwich.id
        ).all()
        for recipe in recipes_for_sandwich:
            resource = db.query(resources.Resource).filter(
                resources.Resource.id == recipe.resource_id
            ).first()
            if not resource or resource.amount < recipe.amount * detail.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough {resource.item} for sandwich {sandwich.sandwich_name}"
                )
            resource.amount -= recipe.amount * detail.quantity
            db.add(resource)

        # Create an order detail
        new_order_detail = order_details.OrderDetail(
            order_id=new_order.id,
            sandwich_id=detail.sandwich_id,
            quantity=detail.quantity,
            price=Decimal(sandwich.price) * detail.quantity,  
            amount=detail.quantity
        )
        db.add(new_order_detail)
        db.commit()
        db.refresh(new_order_detail)

        # Add to order details response
        order_details_response.append({
            "id": new_order_detail.id,
            "order_id": new_order.id,
            "sandwich_id": detail.sandwich_id,
            "sandwich_name": sandwich.sandwich_name,
            "quantity": detail.quantity,
            "price": float(new_order_detail.price),  
            "amount": new_order_detail.amount,
        })

        
        total_price += Decimal(new_order_detail.price) 

    # Update the order's total price
    new_order.total_price = total_price
    db.commit()
    db.refresh(new_order)

    # Build and return the response
    response = {
        "id": new_order.id,
        "customer_id": new_order.customer_id,
        "customer_name": customer.name,
        "description": new_order.description,
        "total_price": float(new_order.total_price),  
        "order_details": order_details_response,
    }

    return response





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
    Retrieve all orders, including customer information and serialized order details.
    """
    try:
        # Join Order with Customer based on customer_id
        result = db.query(order_model.Order, customer_model.Customer).join(
            customer_model.Customer, order_model.Order.customer_id == customer_model.Customer.customer_id
        ).all()

        # Prepare the response
        orders = []
        for order, customer in result:
            # Serialize order details
            serialized_order_details = [
                {
                    "id": detail.id,
                    "order_id": detail.order_id,
                    "sandwich_id": detail.sandwich_id,
                    "quantity": detail.quantity,
                    "price": float(detail.price),  # Convert Decimal to float
                    "amount": detail.amount,
                }
                for detail in order.order_details  # Serialize each OrderDetail object
            ]

            # Build the OrderResponse object
            orders.append(
                OrderResponse(
                    id=order.id,
                    customer_name=customer.name,
                    customer_id=customer.customer_id,
                    description=order.description,
                    total_price=float(order.total_price) if order.total_price else 0.0,
                    order_date=order.order_date,
                    order_details=serialized_order_details,
                )
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return orders





def read_one(db: Session, item_id: int):
    """
    Retrieve a specific order by its ID, including customer information.
    """
    try:
        # Fetch the order and customer using a join
        item = db.query(order_model.Order, customer_model.Customer).join(
            customer_model.Customer, order_model.Order.customer_id == customer_model.Customer.customer_id
        ).filter(order_model.Order.id == item_id).first()

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")

        order, customer = item  # Unpack the tuple

        # Serialize order details
        serialized_order_details = [
            {
                "id": detail.id,
                "order_id": detail.order_id,
                "sandwich_id": detail.sandwich_id,
                "quantity": detail.quantity,
                "price": float(detail.price),  # Convert Decimal to float
                "amount": detail.amount,
            }
            for detail in order.order_details  # Serialize each OrderDetail object
        ]

        # Build the OrderResponse object
        response = OrderResponse(
            id=order.id,
            customer_name=customer.name,
            customer_id=customer.customer_id,
            description=order.description,
            total_price=float(order.total_price) if order.total_price else 0.0,
            order_date=order.order_date,
            order_details=serialized_order_details,
        )
        return response

    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)



def update(db: Session, item_id: int, request: OrderCreate):
    """
    Update an existing order by its ID, including updating order details.
    """
    try:
        # Fetch the existing order
        existing_order = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")

        # Update basic order fields
        existing_order.description = request.description
        existing_order.customer_id = request.customer_id

        # Process order details
        existing_order_details = db.query(order_details.OrderDetail).filter(
            order_details.OrderDetail.order_id == item_id
        ).all()

        # Delete existing order details
        for detail in existing_order_details:
            db.delete(detail)

        # Add updated order details
        total_price = Decimal(0)
        for detail in request.order_details:
            # Validate sandwich
            sandwich = db.query(sandwiches.Sandwich).filter(sandwiches.Sandwich.id == detail.sandwich_id).first()
            if not sandwich:
                raise HTTPException(
                    status_code=404, detail=f"Sandwich with ID {detail.sandwich_id} not found"
                )

            # Validate and deduct resources
            recipes_for_sandwich = db.query(recipes.Recipe).filter(
                recipes.Recipe.sandwich_id == sandwich.id
            ).all()
            for recipe in recipes_for_sandwich:
                resource = db.query(resources.Resource).filter(
                    resources.Resource.id == recipe.resource_id
                ).first()
                if not resource or resource.amount < recipe.amount * detail.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough {resource.item} for sandwich {sandwich.sandwich_name}"
                    )
                # Deduct resource amount
                resource.amount -= recipe.amount * detail.quantity
                db.add(resource)

            # Add new order detail
            new_detail = order_details.OrderDetail(
                order_id=item_id,
                sandwich_id=detail.sandwich_id,
                quantity=detail.quantity,
                price=sandwich.price * detail.quantity,
                amount=detail.quantity
            )
            db.add(new_detail)

            # Update total price
            total_price += new_detail.price

        # Update total price
        existing_order.total_price = total_price

        # Commit changes
        db.commit()
        db.refresh(existing_order)

    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return existing_order

    
def delete(db: Session, item_id: int):
    """
    Delete an order by its ID, including its associated order details.
    """
    try:
        # Fetch the order
        order = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")

        # Explicitly delete associated order details
        db.query(order_details.OrderDetail).filter(order_details.OrderDetail.order_id == item_id).delete(synchronize_session=False)

        # Delete the order
        db.delete(order)
        db.commit()

        # Return a success response
        return {"message": "Order and associated details deleted successfully"}

    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

