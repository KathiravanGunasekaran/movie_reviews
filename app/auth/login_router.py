from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.users import models
from fastapi.security import OAuth2PasswordRequestForm
from app.utils import verify_password
from . import Oauth2, schemas

router = APIRouter(prefix="/api/v1/", tags=['Authorization'])


@router.post("/login", response_model=schemas.TokenDetails)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User is not found")
    if verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username or password might be wrong")
    access_token = Oauth2.create_access_token(data={"user_id": user.id})
    return {"token_type": "bearer", "token": access_token}
