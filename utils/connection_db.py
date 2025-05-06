import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

user = os.getenv("CLEVER_USER")
password = os.getenv("CLEVER_PASSWORD")
host = os.getenv("CLEVER_HOST")
port = os.getenv("CLEVER_PORT")
database = os.getenv("CLEVER_DATABASE")

# Validar variables
if not all([user, password, host, port, database]):
    raise ValueError("Falta una o más variables de entorno necesarias para la conexión a la base de datos.")

# Crear URL de conexión
DATABASE_URL = f"mysql+aiomysql://{user}:{password}@{host}:{port}/{database}"

# Crear engine
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
