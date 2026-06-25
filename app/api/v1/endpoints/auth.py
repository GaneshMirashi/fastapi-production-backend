from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import create_access_token
from app.core.security import verify_password

from app.models.user import User

from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
  ):
  user = db.query(User).filter(
  User.email == form_data.username
  ).first()


  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid credentials"
      )

  valid_password = verify_password(
      form_data.password,
      user.hashed_password
  )

  if not valid_password:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid credentials"
      )

  access_token = create_access_token(
      data={
          "sub": user.email
      }
  )

  return {
      "access_token": access_token,
      "token_type": "bearer"
  }