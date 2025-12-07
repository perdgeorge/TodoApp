from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.users.routes import router as users_router
from src.api.todos.routes import router as todos_router
from src.core.schemas import ErrorSchema
from src.core.exceptions import ErrorException

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])


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


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
