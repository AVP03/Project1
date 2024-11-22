from sqlalchemy.orm import Session
from ..models.ratings import Rating
from ..schemas.ratings import RatingCreate
from fastapi import HTTPException, status
from ..models.ratings import Rating

def get_all_ratings(db: Session):
    return db.query(Rating).all()

def create_rating(db: Session, rating_data: RatingCreate):
    new_rating = Rating(
        review_text=rating_data.review_text,
        rating=rating_data.rating,
        order_id=rating_data.order_id,
        customer_id=rating_data.customer_id
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

# Get ratings by order_id
def get_ratings_by_order(db: Session, order_id: int):
    return db.query(Rating).filter(Rating.order_id == order_id).all()

# Update an existing rating
def update_rating(db: Session, rating_id: int, rating_data: RatingCreate):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    
    if db_rating:
        db_rating.review_text = rating_data.review_text
        db_rating.rating = rating_data.rating
        db_rating.order_id = rating_data.order_id
        db_rating.customer_id = rating_data.customer_id

        db.commit()
        db.refresh(db_rating)
        return db_rating
    else:
        raise HTTPException(status_code=404, detail="Rating not found")

# Delete a rating
def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(db_rating)
    db.commit()
    
    return {"message": "Rating deleted successfully."}
