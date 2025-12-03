from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.users.schemas import CreateUserSchema, GetUserSchema
from src.api.users.services import get_all_users, get_user_by_id
from src.db.postgresql import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=list[GetUserSchema],
)
async def get_users(db: Session = Depends(get_db)) -> list[GetUserSchema]:
    return get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=GetUserSchema,
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    return user


@router.post(
    "/",
    response_model=GetUserSchema,
    status_code=201,
)
async def create_user(user, db: Session = Depends(get_db)) -> CreateUserSchema:
    user = create_user(db, user)
    return user
