from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import order_details as model, recipes as recipe_model, resources as resource_model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    # Fetch the recipe for the sandwich -troy
    recipe_items = db.query(recipe_model.Recipe).filter(recipe_model.Recipe.sandwich_id == request.sandwich_id).all()

    # Subtract resources -troy
    for recipe_item in recipe_items:
        resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == recipe_item.resource_id).first()
        if resource and resource.amount >= recipe_item.amount * request.amount:
            resource.amount -= recipe_item.amount * request.amount
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough {resource.item} available for this order."
            )
    
    # Create the order detail -troy
    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"detail": "Deleted successfully"}
