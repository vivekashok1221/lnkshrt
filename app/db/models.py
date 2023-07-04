from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    """Model for user table."""

    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        pg_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    links: Mapped[list["Link"]] = relationship(back_populates="user", cascade="all, delete")
    tokens: Mapped[list["Token"]] = relationship(back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Link(Base):
    """Model for link table."""

    __tablename__ = "link"

    id: Mapped[UUID] = mapped_column(
        pg_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    original_url: Mapped[str]
    short_url: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="links")


class Token(Base):
    """Model for token table."""

    __tablename__ = "token"

    id: Mapped[UUID] = mapped_column(
        pg_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="tokens")
