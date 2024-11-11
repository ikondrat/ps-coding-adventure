from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from models import User, Board
from db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/boards/")
def create_board(board: Board, session: SessionDep) -> Board:
    session.add(board)

    session.commit()
    session.refresh(board)

    return board


@router.get("/boards/")
def read_boards(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Board]:
    boards = session.exec(select(Board).offset(offset).limit(limit)).all()

    return boards


@router.get("/boards/{access_key}")
def read_board(access_key: str, session: SessionDep) -> Board:
    board = session.exec(
        select(Board).where(Board.access_key == access_key)
    ).one_or_none()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.delete("/boards/{access_key}")
def delete_board(access_key: str, session: SessionDep):
    board = session.exec(
        select(Board).where(Board.access_key == access_key)
    ).one_or_none()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    session.delete(board)
    session.commit()
    return {"ok": True}  # Return a success message
