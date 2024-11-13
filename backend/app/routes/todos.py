from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from models import Todo, TodoInput, TodoView
from db import get_session
from datetime import datetime

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/todos/")
def create_todo(todo_input: TodoInput, session: SessionDep) -> TodoView:
    todo = Todo(**todo_input.model_dump())
    session.add(todo)

    session.commit()
    session.refresh(todo)

    return todo


@router.put("/todos/{todo_id}")
def update_todo(todo_id: UUID, updated_todo: Todo, session: SessionDep) -> TodoView:
    todo = session.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Check for valid state transition
    valid_transitions = {
        "TODO": ["ONGOING"],
        "ONGOING": ["DONE", "TODO"],
        "DONE": ["ONGOING"],
    }

    if updated_todo.state not in valid_transitions[todo.state]:
        raise HTTPException(status_code=400, detail="Invalid state transition")

    todo.title = updated_todo.title
    todo.state = updated_todo.state
    todo.updated_at = datetime.utcnow()  # Assuming last_updated is a field in Todo

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
) -> list[TodoView]:
    todos = session.exec(
        select(Todo).where(Todo.board_id == board_id).offset(offset).limit(limit)
    ).all()
    return todos
