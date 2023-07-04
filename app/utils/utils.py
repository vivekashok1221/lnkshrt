import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import argon2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connections import get_db
from app.db.models import Token, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    """Returns hash of the password."""
    return argon2.using(rounds=4).hash(password)


def check_password(password: str, hash_: str) -> bool:
    """Compares salted-hash against hash of user-inputted password."""
    return argon2.verify(password, hash_)


def generate_token() -> str:
    """Generate a UUID-based token without dashes."""
    return str(uuid.uuid4()).replace("-", "")


async def authenticate_user(username: str, password: str, db_session: AsyncSession) -> User | None:
    """Authenticate a user by checking the username and password."""
    async with db_session.begin():
        user = await db_session.execute(select(User).where(User.username == username))
    user = user.scalar_one_or_none()
    if user and check_password(password, user.password):
        return user
    return None


async def authorize_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> uuid.UUID:
    """Authorize a user based on the provided API key."""
    async with db_session.begin():
        stmt = select(Token).where(Token.token == token)
        token = await db_session.execute(stmt)
    token = token.scalar_one_or_none()
    if token is None:
        raise HTTPException(
            status_code=401, detail="Invalid API key", headers={"WWW-Authenticate": "Bearer"}
        )
    return token.user_id
