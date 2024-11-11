from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from models import Board, Todo
from db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/todos/")
def create_todo(todo: Todo, session: SessionDep) -> Todo:
    session.add(todo)

    session.commit()
    session.refresh(todo)

    return todo


@router.get("/boards/{board_id}/todos/")
def read_todos(
    board_id: UUID,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Todo]:
    todos = session.exec(
        select(Todo).where(Todo.board_id == board_id).offset(offset).limit(limit)
    ).all()
    return todos
