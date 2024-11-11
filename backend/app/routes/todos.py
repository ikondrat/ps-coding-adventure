from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from models import Board, Todo
from db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/todos/")
def create_todo(todo: Todo, session: SessionDep) -> Board:
    session.add(todo)

    session.commit()
    session.refresh(todo)

    return todo
