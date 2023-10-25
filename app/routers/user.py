from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connections import get_db
from app.db.models import Token, User
from app.schemas import SignupResponse, TokenResponse, UserCreate
from app.utils.utils import authenticate_user, generate_token, hash_string

router = APIRouter()


@router.post("/signup")
async def signup(
    user: UserCreate, db_session: Annotated[AsyncSession, Depends(get_db)]
) -> SignupResponse:
    """Endpoint for user signup."""
    username = user.username
    password = user.password
    email = user.email
    try:
        async with db_session.begin():
            db_session.add(User(username=username, email=email, password=hash_string(password)))
    except IntegrityError:
        raise HTTPException(status_code=409, detail="The username or email is already in use.")
    logger.info(f"Created account for {username}.")
    return SignupResponse(message="User registered successfully")


@router.post("/token")
async def create_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Endpoint for creating a token."""
    user = await authenticate_user(credentials.username, credentials.password, db_session)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_token(user.id)

    async with db_session.begin():
        db_session.add(Token(user_id=user.id, token=hash_string(token)))

    return TokenResponse(access_token=token, token_type="bearer")
