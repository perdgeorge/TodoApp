from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.api.users.schemas import CreateUserSchema, GetUserSchema
from src.core.enums import ErrorKind
from src.core.exceptions import ErrorException
from src.core.security import hash_password
from src.db.models.users import User


def get_all_users(db: Session) -> list[GetUserSchema]:
    users = db.query(User).all()
    return [GetUserSchema.model_validate(user) for user in users]


def get_user_by_id(db: Session, user_id: int) -> GetUserSchema:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return GetUserSchema.model_validate(user)
    else:
        raise ErrorException(
            code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            kind=ErrorKind.NOT_FOUND,
            source="get_user_by_id",
        )


def add_user(db: Session, user: User) -> GetUserSchema:
    db.add(user)
    db.commit()
    db.refresh(user)
    return GetUserSchema.model_validate(user)


def create_user(db: Session, user_data: CreateUserSchema) -> GetUserSchema:
    try:
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            hashed_password=hashed_password,
        )
        return add_user(db, new_user)
    except IntegrityError:
        raise ErrorException(
            code=status.HTTP_409_CONFLICT,
            message="Username already exists",
            kind=ErrorKind.CONFLICT,
            source="create_user",
        )
    except Exception:
        raise ErrorException(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Interval Server Error",
            kind=ErrorKind.INTERNAL,
            source="create_user",
        )
