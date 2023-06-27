from typing import Literal

from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping() -> Literal["Pong!"]:
    """Basic ping endpoint."""
    return "Pong!"
