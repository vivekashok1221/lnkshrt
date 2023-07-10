from typing import Literal

from fastapi import FastAPI

from app.routers import link, user

app = FastAPI(title="lnkshrt- Shorten links.")

app.include_router(user.router)
app.include_router(link.router)


@app.get("/ping")
async def ping() -> Literal["Pong!"]:
    """Basic ping endpoint."""
    return "Pong!"
