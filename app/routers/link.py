import urllib
from secrets import token_urlsafe
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.db.connections import get_db
from app.db.models import Link
from app.schemas import LinkCreate, LinkDeleteResponse, LinkResponse
from app.utils.utils import authorize_user, retrieve_url, validate_url_scheme

router = APIRouter()


@router.post("/links")
async def create_link(
    url: LinkCreate,
    user_id: Annotated[UUID, Depends(authorize_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> LinkResponse:
    """Create a new shortened link.

    **Note**:
    The 'shortened_url' field in the response represents just the 'short' part of the URL,
    without the domain part. It follows the pattern 'domain.com/{short}', where '{short}'
    is a unique identifier for the created link. It is up to the frontend client to construct
    the full url.
    """
    original_url = url.url
    custom_url = url.custom_url
    # Normalizing url.
    if custom_url:
        short_url = urllib.parse.quote_plus(custom_url)
    else:
        short_url = token_urlsafe(4)

    original_url = validate_url_scheme(original_url)

    link = Link(original_url=original_url, short_url=short_url, user_id=user_id)
    try:
        async with db_session.begin():
            db_session.add(link)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Custom URL already exists")

    return LinkResponse(shortened_url=short_url)


@router.get("/{short_url}")
async def redirect_url(link: Annotated[Link, Depends(retrieve_url)]) -> RedirectResponse:
    """Redirects to the original URL associated with the given short URL."""
    if link is None:
        raise HTTPException(status_code=404, detail="URL not found")

    # Perform the redirection
    return RedirectResponse(url=link.original_url)


@router.delete("/links/{short_url}")
async def delete_link(
    user_id: Annotated[UUID, Depends(authorize_user)],
    link: Annotated[Link, Depends(retrieve_url)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> LinkDeleteResponse:
    """Endpoint for deleting shortened url."""
    if link is None:
        raise HTTPException(status_code=404, detail="URL not found")

    if user_id != link.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this link")

    async with db_session.begin():
        await db_session.delete(link)

    return LinkDeleteResponse(message="Link deleted successfully")
