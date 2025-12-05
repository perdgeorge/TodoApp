from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.postgresql import get_db
from src.api.todos.services import (
    get_all_todos,
    get_todo_by_id,
    create_todo,
    update_todo_by_id,
    delete_todo_by_id,
)
from src.api.todos.schemas import CreateTodoSchema, GetTodoSchema, UpdateTodoSchema

router = APIRouter()


@router.get("/", response_model=list[GetTodoSchema])
async def Get_Todos(db: Session = Depends(get_db)) -> list[GetTodoSchema]:
    return get_all_todos(db)


@router.get(
    "/{todo_id}",
    response_model=GetTodoSchema,
)
async def Get_Todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo_by_id(db, todo_id)
    return todo


@router.post(
    "/",
    response_model=GetTodoSchema,
    status_code=201,
)
async def Create_todo(
    todo_id: int, todo_data: CreateTodoSchema, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return create_todo(db, todo_data)


@router.put(
    "/{todo_id}",
    response_model=GetTodoSchema,
)
async def Update_Todo(
    todo_id: int, todo_data: UpdateTodoSchema, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return update_todo_by_id(db, todo_id, todo_data)


@router.delete(
    "/{todo_id}",
    response_model=GetTodoSchema,
)
async def Delete_Todo(todo_id: int, db: Session = Depends(get_db)) -> GetTodoSchema:
    return delete_todo_by_id(db, todo_id)
