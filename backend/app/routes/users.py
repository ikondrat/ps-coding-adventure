from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from models import Board, BoardView, User, UserInput, UserView
from db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/users/")
def create_user(user_input: UserInput, session: SessionDep) -> UserView:
    user = User(**user_input.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserView]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/users/{user_id}")
def read_user(user_id: UUID, session: SessionDep) -> UserView:
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/boards")
def read_user_boards(user_id: UUID, session: SessionDep) -> list[BoardView]:
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    boards = user.boards
    if not boards:
        raise HTTPException(status_code=404, detail="Boards not found")

    return boards


@router.put("/users/{user_id}")
def update_user(user_id: UUID, updated_user: UserView, session: SessionDep) -> UserView:
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    user.name = updated_user.name

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@router.post("/signin")
def signin_or_signup(user_input: UserInput, session: SessionDep) -> UserView:
    user = User(**user_input.model_dump())
    existing_user = session.exec(
        select(User).where(User.name == user.name)
    ).one_or_none()
    if existing_user:
        return existing_user

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
