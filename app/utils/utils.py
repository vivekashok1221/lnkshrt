import base64
import urllib.parse
import uuid
from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import argon2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connections import get_db
from app.db.models import Link, Token, User

ALLOWED_SCHEMES = ["http", "https"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_string(plaintext: str) -> str:
    """Returns hash of the password."""
    return argon2.using(rounds=4).hash(plaintext)


def verify_hash(plaintext: str, hash_: str) -> bool:
    """Compares salted-hash against hash of user-inputted password."""
    return argon2.verify(plaintext, hash_)


def generate_token(user_id: uuid.UUID) -> str:
    """Generate a UUID-based token without dashes."""
    encoded_user_id = base64.b64encode(user_id.bytes).decode("utf-8")
    payload = token_urlsafe(32)
    return f"{encoded_user_id}{payload}"


async def authenticate_user(username: str, password: str, db_session: AsyncSession) -> User | None:
    """Authenticate a user by checking the username and password."""
    async with db_session.begin():
        user = await db_session.execute(select(User).where(User.username == username))
    user = user.scalar_one_or_none()
    if user and verify_hash(password, user.password):
        return user
    return None


async def authorize_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> uuid.UUID:
    """Authorize a user based on the provided API key."""
    try:
        # The first 24 characters of the token represent the user ID in base 64 format.
        # It is decoded into bytes and then converted into a UUID object.
        user_id = uuid.UUID(bytes=base64.b64decode(token[:24]))
    except ValueError:
        # The decoded user_id is not a valid UUID.
        raise HTTPException(
            status_code=401, detail="Invalid API key", headers={"WWW-Authenticate": "Bearer"}
        )
    async with db_session.begin():
        stmt = select(Token).where(Token.user_id == user_id)
        token_hashes = await db_session.execute(stmt)
    for token_hash in token_hashes.scalars().all():
        if verify_hash(token, token_hash.token):
            return token_hash.user_id
    raise HTTPException(
        status_code=401, detail="Invalid API key", headers={"WWW-Authenticate": "Bearer"}
    )


async def retrieve_url(
    short_url: str, db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Link | None:
    """Retrieves the original URL associated with the given short URL."""
    short_url = urllib.parse.quote_plus(short_url)
    stmt = select(Link).where(Link.short_url == short_url)
    async with db_session.begin():
        link = await db_session.execute(stmt)
    return link.scalar_one_or_none()


def validate_url_scheme(url: str) -> str:
    """Validates the URL scheme and returns the modified URL with a valid scheme."""
    url_parts = list(urllib.parse.urlsplit(url))
    scheme = url_parts[0]
    if scheme not in ALLOWED_SCHEMES:
        if scheme == "":
            url_parts[0] = "https"
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid URL scheme. Only 'http' and 'https' are allowed.",
            )

    return urllib.parse.urlunsplit(url_parts)
