from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from contextlib import asynccontextmanager

from db import init_db, get_session
from models import User, Board
from routes import users, boards

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app.include_router(users.router)
app.include_router(boards.router)


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
