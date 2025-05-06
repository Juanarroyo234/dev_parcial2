'''Aqui debes construir las operaciones que se te han indicado'''
from data.models import User
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException


async def create_user(
        name: str,
        email: str,
        password: str,
        is_premium: bool = False,
        is_active: bool = True,
        session: AsyncSession  # Dependencia de sesión
):
    new_user = User(
        name=name,
        email=email,
        password=password,  # Asegúrate de hash la contraseña antes de guardarla
        is_premium=is_premium,
        is_active=is_active
    )

    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
