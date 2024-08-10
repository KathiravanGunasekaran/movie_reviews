from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from . import models, schemas
from typing import List
from app.utils import hash_password
router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(req_body: schemas.User, db: Session = Depends(get_db)):
    hashed_password = hash_password(req_body.password)
    req_body.password = hashed_password
    new_user = models.User(**req_body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(path="/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this {user_id} is not found")
    return user


@router.delete(path="/user_id", response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    if user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this {user_id} is not found")
    user_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
