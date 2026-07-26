from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    role: str = "analyst"
):
    """
    Create a new user.

    Default role:
    analyst
    """

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



def get_user_by_email(
    db: Session,
    email: str
):
    """
    Fetch user by email.
    Used during login.
    """

    return (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )



def get_user_by_username(
    db: Session,
    username: str
):
    """
    Fetch user by username.
    """

    return (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )



def get_user_by_id(
    db: Session,
    user_id: int
):
    """
    Fetch user by ID.
    Used by JWT authentication.
    """

    return (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )



def deactivate_user(
    db: Session,
    user_id: int
):
    """
    Disable user account.
    """

    user = get_user_by_id(
        db,
        user_id
    )

    if user:
        user.is_active = False

        db.commit()
        db.refresh(user)

    return user



def update_user_role(
    db: Session,
    user_id: int,
    role: str
):
    """
    Update user RBAC role.

    Allowed examples:
    admin
    analyst
    viewer
    """

    user = get_user_by_id(
        db,
        user_id
    )

    if user:
        user.role = role

        db.commit()
        db.refresh(user)

    return user