import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

USERNAME_RE = re.compile("^[A-Za-z0-9_-]*$")


class UserCreate(BaseModel):
    """Model representing user at signup."""

    username: str
    password: str
    email: EmailStr

    @classmethod
    @field_validator("username")
    def _validate_username(cls, username: str) -> str:
        """Checks if username only contains alphanumeric characters, - and _."""
        if not USERNAME_RE.match(username):
            raise ValueError(
                "Username cannot contain special characters other than underscores and dashes."
            )
        return username

    @classmethod
    @field_validator("password")
    def _validate_password(cls, password: str) -> str:
        """Checks if password is longer than 6 characters."""
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return password


class SignupResponse(BaseModel):
    """Response model for user signup."""

    message: str
    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "User registered successfully"}}
    )


class TokenResponse(BaseModel):
    """Response model for token generation."""

    access_token: str
    token_type: str
    model_config = ConfigDict(
        json_schema_extra={"example": {"access_token": "<token>", "token_type": "bearer"}}
    )


class LinkCreate(BaseModel):
    """Request model for creating a link."""

    url: str
    custom_path: str | None = None


class LinkResponse(BaseModel):
    """Response model for link creation."""

    shortened_url: str


class LinkDeleteResponse(BaseModel):
    """Response model for link deletion."""

    message: str
    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "Link deleted successfully"}}
    )


class PingResponse(BaseModel):
    """Response model for ping endpoint."""

    message: str
    timestamp: datetime
    version: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Pong!",
                "timestamp": "2023-07-12T23:14:46.380726",
                "version": "1.0.0",
            }
        }
    )
