from typing import Literal

from fastapi import FastAPI

from app.routers import user

app = FastAPI()

app.include_router(user.router)


@app.get("/ping")
async def ping() -> Literal["Pong!"]:
    """Basic ping endpoint."""
    return "Pong!"
