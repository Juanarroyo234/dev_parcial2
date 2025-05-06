'''Aqui debes construir las operaciones que se te han indicado'''
from data.models import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

async def create_user(
    name: str,
    email: str,
    password: str,
    is_premium: bool = False,
    is_active: bool = True,
    session: AsyncSession = None  # Mover el parámetro session al final
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
        await session.commit()  # Se realiza el commit para guardar los cambios en la base de datos
        await session.refresh(new_user)  # Refrescamos el objeto para obtener el ID generado
        return new_user  # Retornamos el nuevo usuario
    except IntegrityError:
        await session.rollback()  # Si ocurre un error, revertimos la transacción
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
