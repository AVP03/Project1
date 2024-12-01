from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import ratings as controller
from ..schemas.ratings import RatingCreate, RatingResponse
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)

#READ ALL
@router.get("/", response_model=list[RatingResponse])  
def get_all_ratings(db: Session = Depends(get_db)):
    return controller.get_all_ratings(db=db)

#CREATE
@router.post("/", response_model=RatingResponse)
def create_rating(rating_data: RatingCreate, db: Session = Depends(get_db)):
    return controller.create_rating(db=db, rating_data=rating_data)

#READ ONE
@router.get("/order/{order_id}", response_model=list[RatingResponse])
def get_ratings(order_id: int, db: Session = Depends(get_db)):
    return controller.get_ratings_by_order(db=db, order_id=order_id)

#UPDATE
@router.put("/{rating_id}", response_model=RatingResponse)
def update_rating(rating_id: int, rating_data: RatingCreate, db: Session = Depends(get_db)):
    return controller.update_rating(db=db, rating_id=rating_id, rating_data=rating_data)

#DELETE
@router.delete("/{rating_id}", response_model=dict)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    return controller.delete_rating(db=db, rating_id=rating_id)