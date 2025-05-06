'''Aqui debes construir las operaciones que se te han indicado'''
# operations/operations_db.py

from sqlmodel import SQLModel, select
from data.models import User  # Asegúrate de usar SQLModel, no declarative_base
from utils.connection_db import get_session
from sqlalchemy.exc import IntegrityError

async def create_user(name: str, email: str, password: str):
    async for session in get_session():
        new_user = User(name=name, email=email, password=password)
        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError:
            await session.rollback()
            raise ValueError("El correo electrónico ya está registrado.")
