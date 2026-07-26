from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)

from app.services.user_service import create_user
from app.services.audit_service import create_audit_log

from app.models.user import User

from app.core.security import verify_password
from app.core.jwt import create_access_token


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# Register User
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        (User.email == user.email) |
        (User.username == user.username)
    ).first()


    if existing_user:

        create_audit_log(
            db=db,
            action="REGISTER_FAILED",
            resource="AUTH",
            status="FAILED",
            details=f"Registration failed for {user.email}. User already exists."
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )


    new_user = create_user(
        db,
        user.username,
        user.email,
        user.password
    )


    create_audit_log(
        db=db,
        action="REGISTER",
        resource="AUTH",
        user_id=new_user.id,
        status="SUCCESS",
        details="User registered successfully"
    )


    return new_user




# Login User
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

        create_audit_log(
            db=db,
            action="LOGIN_FAILED",
            resource="AUTH",
            status="FAILED",
            details=f"Login failed. User not found: {user.email}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


    if not verify_password(
        user.password,
        db_user.hashed_password
    ):

        create_audit_log(
            db=db,
            action="LOGIN_FAILED",
            resource="AUTH",
            user_id=db_user.id,
            status="FAILED",
            details="Invalid password"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


    if not db_user.is_active:

        create_audit_log(
            db=db,
            action="LOGIN_FAILED",
            resource="AUTH",
            user_id=db_user.id,
            status="FAILED",
            details="Login attempt for inactive user"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )


    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "username": db_user.username,
            "email": db_user.email,
            "role": db_user.role
        }
    )


    create_audit_log(
        db=db,
        action="LOGIN",
        resource="AUTH",
        user_id=db_user.id,
        status="SUCCESS",
        details="User login successful"
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }