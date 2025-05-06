from data.models import User
from utils.connection_db import get_session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession  # Importación de AsyncSession
from fastapi import Depends

async def create_user(
    name: str,
    email: str,
    password: str,
    is_premium: bool = False,
    is_active: bool = True,
    session: AsyncSession = Depends(get_session)  # Dependencia de sesión
):
    new_user = User(
        name=name,
        email=email,
        password=password,  # Asegúrate de manejar el hash de la contraseña
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
