from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.users.schemas import CreateUserSchema, GetUserSchema
from src.api.users.services import get_all_users, get_user_by_id, create_user
from src.core.schemas import ErrorResponse
from src.db.postgresql import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=list[GetUserSchema],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Get_All_Users(db: Session = Depends(get_db)) -> list[GetUserSchema]:
    return get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=GetUserSchema,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Get_User_By_Id(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    return user


@router.post(
    "/",
    response_model=GetUserSchema,
    status_code=201,
    responses={
        409: {"model": ErrorResponse, "description": "User already exists"},
        422: {"model": ErrorResponse, "description": "Invalid User input format"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Register_User(
    user: CreateUserSchema, db: Session = Depends(get_db)
) -> GetUserSchema:
    return create_user(db, user)
