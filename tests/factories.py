from faker import Faker
from src.api.users.schemas import CreateUserSchema
from src.api.todos.schemas import CreateTodoSchema

fake = Faker()


def make_user_payload() -> CreateUserSchema:
    return CreateUserSchema(
        username=fake.unique.user_name(),
        password=fake.password(
            length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
        ),
    )


def make_todo_payload() -> CreateTodoSchema:
    return CreateTodoSchema(
        title=fake.unique.title(),
        description=fake.description(length=100),
    )
