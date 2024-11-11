from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from contextlib import asynccontextmanager

from db import init_db, get_session
from routes import users, boards, todos

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app.include_router(users.router)
app.include_router(boards.router)
app.include_router(todos.router)
