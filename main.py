from fastapi import FastAPI, HTTPException, Depends
from typing import List
from data.models import User, UserCreate, UserRead
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.connection_db import get_session, init_db
from operations.operations_db import create_user

# Crear la instancia de la aplicación FastAPI
app = FastAPI()


# Función de inicio para gestionar la base de datos durante el ciclo de vida de la aplicación
@app.on_event("startup")
async def on_startup():
    await init_db()  # Llamamos a la función de inicialización de la DB


@app.on_event("shutdown")
async def on_shutdown():
    pass  # Aquí podríamos cerrar conexiones si fuera necesario


# Endpoint para la creación de un nuevo usuario
@app.post("/users", response_model=UserRead)
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Llamamos a la función para crear el usuario
        new_user = await create_user(
            name=user.name,
            email=user.email,
            password=user.password,
            is_premium=user.is_premium,
            is_active=user.is_active,
            session=session  # Pasamos la sesión
        )
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")


# Endpoint para listar todos los usuarios
@app.get("/users", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()  # Convertimos el resultado en una lista de usuarios
    return users


# Endpoint para obtener un usuario por su ID
@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()  # Obtenemos el usuario o None si no existe
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# Endpoint para actualizar el estado de un usuario
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

    # Solo actualizamos los valores que recibimos en la petición
    if is_premium is not None:
        user.is_premium = is_premium
    if is_active is not None:
        user.is_active = is_active

    # Guardamos los cambios
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

@app.get("/users/active", response_model=List[UserRead])
async def get_active_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.is_active == True))
    active_users = result.scalars().all()
    return active_users


# Punto de entrada para verificar que la API está funcionando
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Users API"}

