'''Aqui debes consignar el modelo que se te indico en el parcial
Escribe aquí el que te corresponde.

'''

# data/models.py

from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    is_premium: bool = Field(default=False)
    is_active: bool = Field(default=True)

class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    is_premium: Optional[bool] = False
    is_active: Optional[bool] = True

class UserRead(SQLModel):
    id: int
    name: str
    email: str
    is_premium: bool
    is_active: bool


