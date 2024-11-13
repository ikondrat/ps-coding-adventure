from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

from db import init_db, get_session
from routes import users, boards, todos

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_db()


app.include_router(users.router)
app.include_router(boards.router)
app.include_router(todos.router)
