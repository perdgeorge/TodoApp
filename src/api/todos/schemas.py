from datetime import datetime
from pydantic import Field
from src.api.schemas import BaseSchema


class TodoSchema(BaseSchema):
    title: str = Field(
        ...,
        examples=["Buy groceries"],
    )
    description: str = Field(..., examples=["Milk, Bread, Eggs"])


class GetTodoSchema(TodoSchema):
    id: int = Field(..., examples=[1])
    completed_at: datetime | None = Field(..., examples=["2025-11-14T12:00:00Z"])


class CreateTodoSchema(TodoSchema):
    pass


class UpdateTodoSchema(TodoSchema):
    pass


class DeleteTodoSchema(TodoSchema):
    id: int = Field(..., examples=[1])
