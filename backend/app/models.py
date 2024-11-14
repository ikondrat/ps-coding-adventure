from typing import Optional
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

    todos: list["Todo"] = Relationship(back_populates="user", cascade_delete=True)


class UserInput(SQLModel):
    name: str


class UserView(SQLModel):
    id: UUID
    name: str


class Board(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    access_key: str | None = Field(default_factory=lambda: secrets.token_hex(16))

    # Define a relationship to User
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="boards")

    todos: list["Todo"] = Relationship(back_populates="board", cascade_delete=True)


class BoardInput(SQLModel):
    name: str
    access_key: str | None = Field(default_factory=lambda: secrets.token_hex(16))


class BoardView(SQLModel):
    id: UUID
    name: str
    access_key: str


class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    state: TodoState = Field(default=TodoState.TODO)
    state_details: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Define a relationship to User
    user_id: UUID = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="todos")

    # Define a relationship to Board
    board_id: UUID = Field(default=None, foreign_key="board.id")
    board: Board | None = Relationship(back_populates="todos")


class TodoInput(SQLModel):
    title: str
    state: Optional[TodoState] = TodoState.TODO
    state_details: str
    user_id: UUID
    board_id: UUID


class TodoView(SQLModel):
    id: UUID
    title: str
    state: TodoState
    state_details: str
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    board_id: UUID
