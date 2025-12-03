from pydantic import Field
from src.api.schemas import BaseSchema


class UserSchema(BaseSchema):
    username: str = Field(..., example=["exampleuser"])


class CreateUserSchema(UserSchema):
    password: str = Field(..., min_length=8, examples=["password123"])


class GetUserSchema(UserSchema):
    id: int = Field(..., examples=[1])
