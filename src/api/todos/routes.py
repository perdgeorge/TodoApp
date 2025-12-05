from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from src.db.postgresql import get_db
from src.api.todos.services import get_all_todos, get_todo_by_id, create_todo
from src.api.todos.schemas import (
    CreateTodoSchema,
    GetTodoSchema,
)

router = APIRouter()


@router.get("/", response_model=list[GetTodoSchema])
async def get_todos(db: Session = Depends(get_db)) -> list[GetTodoSchema]:
    return get_all_todos(db)


@router.get(
    "/{user_id}",
    response_model=GetTodoSchema,
)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo_by_id(db, todo_id)
    return todo


@router.post(
    "/",
    response_model=GetTodoSchema,
    status_code=201,
)
async def register_todo(
    todo_data: CreateTodoSchema = Body(...), db: Session = Depends(get_db)
) -> GetTodoSchema:
    return create_todo(db, todo_data)
