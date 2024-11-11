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


@router.get("/boards/{board_id}")
def read_board(board_id: UUID, session: SessionDep) -> Board:
    statement = select(Board).where(Board.id == board_id)
    board = session.exec(statement)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.put("/boards/{board_id}")
def update_board(
    user_id: UUID, board_id: UUID, updated_board: Board, session: SessionDep
) -> Board:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    board = session.get(Board, board_id)
    if not board or board not in user.boards:
        raise HTTPException(status_code=404, detail="Board not found")

    # Update fields
    board.title = updated_board.title
    board.description = (
        updated_board.description
    )  # Assuming Board has a description field

    session.add(board)
    session.commit()
    session.refresh(board)
    return board  # Return the updated board


@router.delete("/boards/{board_id}")
def delete_board(user_id: UUID, board_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    board = session.get(Board, board_id)
    if not board or board not in user.boards:
        raise HTTPException(status_code=404, detail="Board not found")

    session.delete(board)
    session.commit()
    return {"ok": True}  # Return a success message
