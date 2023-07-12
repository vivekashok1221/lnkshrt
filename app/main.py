import tomllib
from datetime import datetime

from fastapi import FastAPI

from app.routers import link, user
from app.schemas import PingResponse

with open("pyproject.toml", "rb") as f:
    project_metadata = tomllib.load(f)["tool"]["poetry"]
    version = project_metadata["version"]
    # description = project_metadata["description"]

app = FastAPI(title="lnkshrt- Shorten links.", version=version)


@app.get("/ping")
async def ping() -> PingResponse:
    """Basic ping endpoint."""
    return PingResponse(message="Pong!", timestamp=datetime.utcnow(), version=version)


app.include_router(user.router)
app.include_router(link.router)
