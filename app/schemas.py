import re

from pydantic import BaseModel, EmailStr, validator

USERNAME_RE = re.compile("^[A-Za-z0-9_-]*$")


class UserCreate(BaseModel):
    """Model representing user at signup."""

    username: str
    password: str
    email: EmailStr

    @validator("username")
    def _validate_username(cls, username: str) -> str:
        """Checks if username only contains alphanumeric characters, - and _."""
        if not USERNAME_RE.match(username):
            raise ValueError(
                "Username cannot contain special characters other than underscores and dashes."
            )
        return username

    @validator("password")
    def _validate_password(cls, password: str) -> str:
        """Checks if password is longer than 6 characters."""
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return password


class SignupResponse(BaseModel):
    """Response model for user signup."""

    message: str

    class Config:
        """Extra schema information for the model."""

        schema_extra = {"example": {"message": "User registered successfully"}}


class TokenResponse(BaseModel):
    """Response model for token generation."""

    access_token: str
    token_type: str

    class Config:
        """Extra schema information for the model."""

        schema_extra = {"example": {"access_token": "<token>", "token_type": "bearer"}}


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

    class Config:
        """Extra schema information for the model."""

        schema_extra = {"example": {"message": "Link deleted successfully"}}
