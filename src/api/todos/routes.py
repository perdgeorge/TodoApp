from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.postgresql import get_db
from src.api.todos.services import (
    get_all_todos,
    get_todo_by_id,
    create_todo,
    update_todo,
)
from src.api.todos.schemas import CreateTodoSchema, GetTodoSchema, UpdateTodoSchema

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
    todo_id: int, todo_data: CreateTodoSchema, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return create_todo(db, todo_data)


@router.put(
    "/{user_id}",
    response_model=GetTodoSchema,
)
async def update_todoo(
    todo_id: int, todo_data: UpdateTodoSchema, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return update_todo(db, todo_id, todo_data)
