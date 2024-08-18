from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.models import Base
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
DB_URL = f"sqlite+aiosqlite:///{os.path.join(base_dir, 'eshop.db')}"

engine = create_async_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def generate_session():
    async with SessionLocal() as session:
        yield session
