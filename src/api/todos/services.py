from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.api.todos.schemas import (
    GetTodoSchema,
    CreateTodoSchema,
    UpdateTodoSchema,
)
from src.core.enums import ErrorKind
from src.core.exceptions import ErrorException
from src.db.models.todos import Todo


def get_all_todos(db: Session) -> list[GetTodoSchema]:
    todos = db.query(Todo).all()
    return [GetTodoSchema.model_validate(todo) for todo in todos]


def get_todo_by_id(db: Session, todo_id: int) -> GetTodoSchema:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return GetTodoSchema.model_validate(todo)
    else:
        raise ErrorException(
            code=status.HTTP_404_NOT_FOUND,
            message="Task not found",
            kind=ErrorKind.NOT_FOUND,
            source={"get_todo_by_id"},
        )


def get_completed_todos(db: Session) -> list[GetTodoSchema]:
    todos = db.query(Todo).filter(Todo.completed_at.is_not(None)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="Completed Tasks not found")
    return [GetTodoSchema.model_validate(todo) for todo in todos]


def get_uncompleted_todos(db: Session) -> list[GetTodoSchema]:
    todos = db.query(Todo).filter(Todo.completed_at.is_(None)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="Uncompleted Tasks not found")
    return [GetTodoSchema.model_validate(todo) for todo in todos]


def add_todo(db: Session, todo: Todo) -> GetTodoSchema:
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return GetTodoSchema.model_validate(todo)


def create_todo(
    db: Session,
    todo_data: CreateTodoSchema,
) -> GetTodoSchema:
    try:
        new_todo = Todo(title=todo_data.title, description=todo_data.description)
        return add_todo(db, new_todo)
    except IntegrityError:
        raise ErrorException(
            code=status.HTTP_409_CONFLICT,
            message="Task title already exists",
            kind=ErrorKind.CONFLICT,
            source="create_todo",
        )


def update_todo_by_id(
    db: Session, todo_id: int, todo_data: UpdateTodoSchema
) -> GetTodoSchema:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        db.commit()
        db.refresh(todo)
        return GetTodoSchema.model_validate(todo)
    except IntegrityError:
        raise ErrorException(
            code=status.HTTP_409_CONFLICT,
            message="Task title already exists",
            kind=ErrorKind.CONFLICT,
            source="update_todo_by_id",
        )


def update_todo_as_completed(
    db: Session,
    todo_id: int,
) -> GetTodoSchema:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        if todo.completed_at is None:
            todo.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(todo)
        return GetTodoSchema.model_validate(todo)
    except IntegrityError:
        raise ErrorException(
            code=status.HTTP_409_CONFLICT,
            message="Task is already completed",
            kind=ErrorKind.CONFLICT,
            source="update_todo_as_completed",
        )


def delete_todo_by_id(db: Session, todo_id: int) -> GetTodoSchema:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        db.delete(todo)
        db.commit()
        return GetTodoSchema.model_validate(todo)
