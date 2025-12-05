from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.users.schemas import CreateUserSchema, GetUserSchema
from src.core.security import hash_password
from src.db.models.users import User


def get_all_users(db: Session) -> list[GetUserSchema]:
    users = db.query(User).all()
    return [GetUserSchema.model_validate(user) for user in users]


def get_user_by_id(db: Session, user_id: int) -> GetUserSchema:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUserSchema.model_validate(user)


def add_user(db: Session, user: User) -> GetUserSchema:
    db.add(user)
    db.commit()
    db.refresh(user)
    return GetUserSchema.model_validate(user)


def create_user(db: Session, user_data: CreateUserSchema) -> GetUserSchema:
    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )
    return add_user(db, new_user)
