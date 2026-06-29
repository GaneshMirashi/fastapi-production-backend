from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.security import hash_password
from app.core.security import verify_password

from app.repositories.user_repository import UserRepository

class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        name: str,
        email: str,
        password: str
    ):
        existing_user = UserRepository.get_user_by_email(
            db,
            email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = hash_password(password)

        return UserRepository.create_user(
            db=db,
            name=name,
            email=email,
            hashed_password=hashed_password
        )

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ):
        user = UserRepository.get_user_by_email(
            db,
            email
        )

        if not user:
            return None

        valid_password = verify_password(
            password,
            user.hashed_password
        )

        if not valid_password:
            return None

        return user

    @staticmethod
    def generate_token(
        email: str
    ):
        return create_access_token(
            data={
                "sub": email
            }
        )