from fastapi import FastAPI
from src.api.users.routes import router as users_router


app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
