from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserResponse,
    UserRoleUpdate
)

from app.dependencies.permissions import require_role
from app.services.user_service import (
    update_user_role,
    deactivate_user
)


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)



@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[
        Depends(require_role(["admin"]))
    ]
)
def list_users(
    db: Session = Depends(get_db)
):

    return db.query(User).all()



@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[
        Depends(require_role(["admin"]))
    ]
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user



@router.put(
    "/{user_id}/role",
    response_model=UserResponse,
    dependencies=[
        Depends(require_role(["admin"]))
    ]
)
def change_role(
    user_id:int,
    data:UserRoleUpdate,
    db:Session=Depends(get_db)
):

    user = update_user_role(
        db,
        user_id,
        data.role
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user




@router.put(
    "/{user_id}/deactivate",
    response_model=UserResponse,
    dependencies=[
        Depends(require_role(["admin"]))
    ]
)
def disable_user(
    user_id:int,
    db:Session=Depends(get_db)
):

    user = deactivate_user(
        db,
        user_id
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user