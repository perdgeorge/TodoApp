from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.schemas import ErrorResponse
from src.db.postgresql import get_db
from src.api.todos.services import (
    get_all_todos,
    get_todo_by_id,
    get_completed_todos,
    create_todo,
    get_uncompleted_todos,
    update_todo_as_completed,
    update_todo_by_id,
    delete_todo_by_id,
)
from src.api.todos.schemas import (
    CreateTodoSchema,
    GetTodoSchema,
    UpdateTodoSchema,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[GetTodoSchema],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Get_Tasks(db: Session = Depends(get_db)) -> list[GetTodoSchema]:
    return get_all_todos(db)


@router.get(
    "/{todo_id}",
    response_model=GetTodoSchema,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Get_Task_By_Id(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo_by_id(db, todo_id)
    return todo


@router.get(
    "/completed/",
    response_model=list[GetTodoSchema],
    responses={
        404: {"model": ErrorResponse, "description": "No Completed tasks found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Get_Completed_Tasks(db: Session = Depends(get_db)) -> list[GetTodoSchema]:
    return get_completed_todos(db)


@router.get(
    "/uncompleted/",
    response_model=list[GetTodoSchema],
    responses={
        404: {"model": ErrorResponse, "description": "No uncompleted tasks found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Get_Uncompleted_Tasks(db: Session = Depends(get_db)) -> list[GetTodoSchema]:
    return get_uncompleted_todos(db)


@router.post(
    "/",
    response_model=GetTodoSchema,
    status_code=201,
    responses={
        409: {"model": ErrorResponse, "description": "Task title already exists"},
        422: {"model": ErrorResponse, "description": "Invalid Task input format"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Create_Task(
    todo: CreateTodoSchema, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return create_todo(db, todo)


@router.put(
    "/{todo_id}",
    response_model=GetTodoSchema,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        409: {"model": ErrorResponse, "description": "Task title already exists"},
        422: {"model": ErrorResponse, "description": "Invalid Task input format"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Update_Task(
    todo_id: int, todo: UpdateTodoSchema, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return update_todo_by_id(db, todo_id, todo)


@router.put(
    "/{todo_id}/complete",
    response_model=GetTodoSchema,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        409: {"model": ErrorResponse, "description": "Task is already completed"},
        422: {"model": ErrorResponse, "description": "Invalid Task input format"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Mark_Task_as_completed(
    todo_id: int, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return update_todo_as_completed(db, todo_id)


@router.delete(
    "/{todo_id}",
    response_model=GetTodoSchema,
    status_code=200,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def Delete_Task_by_id(
    todo_id: int, db: Session = Depends(get_db)
) -> GetTodoSchema:
    return delete_todo_by_id(db, todo_id)
