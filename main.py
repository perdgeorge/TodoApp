from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.users.routes import router as users_router
from src.api.todos.routes import router as todos_router
from src.api.auth.routes import router as auth_router
from src.core.logging import setup_logging
from src.core.schemas import ErrorSchema
from src.core.exceptions import ErrorException

setup_logging()

app = FastAPI()


@app.exception_handler(ErrorException)
async def exception_handler(request: Request, exc: ErrorException):
    error_response = ErrorSchema(
        code=exc.code,
        message=exc.message,
        kind=exc.kind,
        source=exc.source,
    )
    return JSONResponse(
        status_code=exc.code,
        content=error_response.as_exception_response(),
    )


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])
app.include_router(auth_router, tags=["auth"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
