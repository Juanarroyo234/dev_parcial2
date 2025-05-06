'''Aqui debes consignar el modelo que se te indico en el parcial
Escribe aquí el que te corresponde.

'''

# data/models.py

from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

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

class TaskStatus(str, Enum):
    pendiente = "pendiente"
    ejecucion = "ejecución"
    realizada = "realizada"
    cancelada = "cancelada"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.pendiente)

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = Field(default=None)
    status: Optional[TaskStatus] = TaskStatus.pendiente


class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
