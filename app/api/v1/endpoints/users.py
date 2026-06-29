from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.api.deps import get_current_user

from app.core.database import get_db

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
user: UserCreate,
db: Session = Depends(get_db)
):
    return AuthService.register_user(
    db=db,
    name=user.name,
    email=user.email,
    password=user.password
    )

@router.get("/", response_model=list[UserResponse])
def get_users(
db: Session = Depends(get_db)
):
    return UserRepository.get_all_users(db)

@router.get("/me", response_model=UserResponse)
def get_current_logged_in_user(
current_user: User = Depends(get_current_user)
):
    return current_user
