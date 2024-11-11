from typing import Annotated
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
import secrets


class TodoState(str, Enum):
    TODO = "TODO"
    ONGOING = "ONGOING"
    DONE = "DONE"


class User(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)

    boards: list["Board"] = Relationship(back_populates="user", cascade_delete=True)
    # Define a relationship to Todo with cascade delete
    # todos: list["Todo"] | None = Relationship(
    #     back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    # )

    # Define a relationship to Board with cascade delete
    # board: Board | None = Relationship(
    #     back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    # )


class Board(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    access_key: str | None = Field(default_factory=lambda: secrets.token_hex(16))

    # Define a relationship to User
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="boards")

    # Define a relationship to Todo with cascade delete
    # todos: list["Todo"] | None = Relationship(
    #     back_populates="board",
    #     cascade_delete=True,
    # )


# class Todo(SQLModel, table=True):
#     id: UUID | None = Field(default_factory=uuid4, primary_key=True)
#     title: str
#     state: TodoState = Field(default=TodoState.TODO)
#     last_updated: datetime = Field(default_factory=datetime.utcnow)

#     # Define a relationship to User
#     user_id: UUID | None = Field(default=None, foreign_key="user.id")
#     user: User = Relationship(back_populates="todos")

#     # Define a relationship to Board
#     board_id: UUID | None = Field(default=None, foreign_key="board.id")
#     board: Board = Relationship(back_populates="todos")
