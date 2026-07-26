from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)
from app.services.user_service import create_user
from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
    	(User.email == user.email) |
    	(User.username == user.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )


    return create_user(
        db,
        user.username,
        user.email,
        user.password
    )


@router.post(
    "/login",
    response_model=TokenResponse
)

def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    token = create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }