from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from contextlib import asynccontextmanager

from db import init_db, get_session
from models import User, Board

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/users/{user_id}")
def read_user(user_id: UUID, session: SessionDep) -> User:
    print(f"Looking for user with ID: {user_id}")
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@app.post("/boards/")
def create_board(board: Board, session: SessionDep) -> Board:
    session.add(board)
    session.commit()
    session.refresh(board)

    return board


@app.get("/boards/")
def read_boards(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Board]:
    boards = session.exec(select(Board).offset(offset).limit(limit)).all()

    return boards


@app.get("/boards/{board_id}")
def read_board(user_id: UUID, board_id: UUID, session: SessionDep) -> Board:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    board = session.get(Board, board_id)
    if not board or board not in user.boards:
        raise HTTPException(status_code=404, detail="Board not found")

    return board  # Return the specific board


@app.put("/boards/{board_id}")
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


@app.delete("/boards/{board_id}")
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


# @app.post("/boards/{board_id}/todos/")
# def create_todo_for_board(board_id: UUID, todo: Todo, session: SessionDep) -> Todo:
#     board = session.get(Board, board_id)
#     if not board:
#         raise HTTPException(status_code=404, detail="Board not found")

#     session.add(todo)
#     board.todos.append(todo)  # Assuming Board has a todos relationship
#     session.commit()
#     session.refresh(todo)
#     return todo


# @app.get("/boards/{board_id}/todos/")
# def read_todos_for_board(board_id: UUID, session: SessionDep) -> list[Todo]:
#     board = session.get(Board, board_id)
#     if not board:
#         raise HTTPException(status_code=404, detail="Board not found")

#     return board.todos  # Return the list of todos for the board


# @app.get("/boards/{board_id}/todos/{todo_id}")
# def read_todo_for_board(board_id: UUID, todo_id: UUID, session: SessionDep) -> Todo:
#     board = session.get(Board, board_id)
#     if not board:
#         raise HTTPException(status_code=404, detail="Board not found")

#     todo = session.get(Todo, todo_id)
#     if not todo or todo not in board.todos:
#         raise HTTPException(status_code=404, detail="Todo not found")

#     return todo  # Return the specific todo


# @app.put("/boards/{board_id}/todos/{todo_id}")
# def update_todo_for_board(
#     board_id: UUID, todo_id: UUID, updated_todo: Todo, session: SessionDep
# ) -> Todo:
#     board = session.get(Board, board_id)
#     if not board:
#         raise HTTPException(status_code=404, detail="Board not found")

#     todo = session.get(Todo, todo_id)
#     if not todo or todo not in board.todos:
#         raise HTTPException(status_code=404, detail="Todo not found")

#     # Update fields
#     todo.title = updated_todo.title
#     todo.description = updated_todo.description  # Assuming Todo has a description field
#     todo.completed = updated_todo.completed  # Assuming Todo has a completed field

#     session.add(todo)
#     session.commit()
#     session.refresh(todo)
#     return todo  # Return the updated todo


# @app.delete("/boards/{board_id}/todos/{todo_id}")
# def delete_todo_for_board(board_id: UUID, todo_id: UUID, session: SessionDep):
#     board = session.get(Board, board_id)
#     if not board:
#         raise HTTPException(status_code=404, detail="Board not found")

#     todo = session.get(Todo, todo_id)
#     if not todo or todo not in board.todos:
#         raise HTTPException(status_code=404, detail="Todo not found")

#     session.delete(todo)
#     session.commit()
#     return {"ok": True}  # Return a success message
