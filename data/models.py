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

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str


