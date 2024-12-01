from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Resources"],
    prefix="/resources"
)

#CREATE
@router.post("/", response_model=schema.Resource)
def create(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

#READ ALL
@router.get("/", response_model=list[schema.Resource])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

#READ ONE
@router.get("/{resource_id}", response_model=schema.Resource)  # Updated here
def read_one(resource_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, resource_id=resource_id)  # Updated here

#UPDATE
@router.put("/{resource_id}", response_model=schema.Resource)  # Updated here
def update(resource_id: int, request: schema.ResourceUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, resource_id=resource_id, request=request)  # Updated here

#DELETE
@router.delete("/{resource_id}")  # Updated here
def delete(resource_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, resource_id=resource_id)  # Updated here
