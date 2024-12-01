from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Sandwiches"],
    prefix="/sandwiches"
)

#CREATE
@router.post("/", response_model=schema.Sandwich)
def create(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

#READ ALL
@router.get("/", response_model=list[schema.Sandwich])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

#READ ONE
@router.get("/{item_id}", response_model=schema.Sandwich)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)

#UPDATE
@router.put("/{item_id}", response_model=schema.Sandwich)
def update(item_id: int, request: schema.SandwichUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)

#DELETE
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
