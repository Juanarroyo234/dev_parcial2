from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from utils.connection_db import init_db, get_session
from operations.operations_db import create_user
from data.models import UserCreate, UserRead
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from typing import List
from data.models import User
from utils.connection_db import get_session



# Inicialización de la base de datos con lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="API Usuarios", lifespan=lifespan)

# Endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/users", response_model=UserRead)
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        new_user = await create_user(user.name, user.email, user.password)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="El correo ya existe")

@app.get("/users", response_model=List[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
