from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.todos.schemas import (
    GetTodoSchema,
    CreateTodoSchema,
    # UpdateTodoSchema,
    # DeleteTodoSchema,
)
from src.db.models.todos import Todo


def get_all_todos(db: Session) -> list[GetTodoSchema]:
    todos = db.query(Todo).all()
    return [GetTodoSchema.model_validate(todo) for todo in todos]


def get_todo_by_id(db: Session, todo_id: int) -> GetTodoSchema:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return GetTodoSchema.model_validate(todo)


def add_todo(db: Session, todo: Todo) -> GetTodoSchema:
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return GetTodoSchema.model_validate(todo)


def create_todo(
    db: Session,
    todo_data: CreateTodoSchema,
) -> GetTodoSchema:
    new_todo = Todo(title=todo_data.title, description=todo_data.description)
    return add_todo(db, new_todo)


def update_todo(
    db: Session, todo_id: int, todo_data: CreateTodoSchema
) -> GetTodoSchema:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    try:
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        db.commit()
        db.refresh(todo)
        return GetTodoSchema.model_validate(todo)
    except HTTPException:
        raise HTTPException(status_code=409, detail="Todo title already exists")
