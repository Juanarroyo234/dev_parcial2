from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from data.models import User, UserCreate, UserRead, Task, TaskCreate, TaskRead
from data.models import TaskStatus  # para usar en operaciones
from utils.connection_db import get_session, init_db
from operations.operations_db import create_user, create_task  # asegúrate de tener ambas funciones


# Crear la instancia de la aplicación FastAPI
app = FastAPI()


# Función de inicio para gestionar la base de datos durante el ciclo de vida de la aplicación
@app.on_event("startup")
async def on_startup():
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    pass


# ---------- USERS ENDPOINTS ----------

@app.post("/users", response_model=UserRead)
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        new_user = await create_user(
            name=user.name,
            email=user.email,
            password=user.password,
            is_premium=user.is_premium,
            is_active=user.is_active,
            session=session
        )
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")


@app.get("/users", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@app.put("/users/{user_id}", response_model=UserRead)
async def update_user_status(
    user_id: int,
    is_premium: bool = None,
    is_active: bool = None,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if is_premium is not None:
        user.is_premium = is_premium
    if is_active is not None:
        user.is_active = is_active

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@app.get("/users/active", response_model=List[UserRead])
async def get_active_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.is_active == True))
    active_users = result.scalars().all()
    return active_users


@app.get("/users/active-premium", response_model=List[UserRead])
async def get_active_premium_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.is_active == True, User.is_premium == True)
    )
    users = result.scalars().all()
    return users


# ---------- TASKS ENDPOINTS ----------

@app.post("/tasks", response_model=TaskRead)
async def add_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    try:
        new_task = await create_task(
            title=task.title,
            description=task.description,
            status=task.status,
            session=session
        )
        return new_task
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Error al crear la tarea")


@app.get("/tasks", response_model=List[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@app.put("/tasks/{task_id}/status", response_model=TaskRead)
async def update_task_status(
    task_id: int,
    status: TaskStatus,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task.status = status
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


# ---------- ROOT ----------

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Users & Tasks API"}
