from pydantic import Field
from src.api.schemas import BaseSchema


class TodoSchema(BaseSchema):
    title: str = Field(
        ...,
    )
    description: str = Field(
        ...,
    )


class GetTodoSchema(TodoSchema):
    id: int = Field(..., examples=[1])


class CreateTodoSchema(TodoSchema):
    pass


class UpdateTodoSchema(TodoSchema):
    title: str = Field(
        ...,
    )
    description: str = Field(
        ...,
    )


class DeleteTodoSchema(GetTodoSchema):
    pass
