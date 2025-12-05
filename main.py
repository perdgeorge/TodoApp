from fastapi import FastAPI
from src.api.users.routes import router as users_router
from src.api.todos.routes import router as todos_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
