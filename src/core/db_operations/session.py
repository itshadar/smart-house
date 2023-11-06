from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session

from src.config import async_database_uri, database_uri, env

engine = create_engine(database_uri)
async_engine = create_async_engine(async_database_uri)


if env == "dev":
    engine.echo = True
    async_engine.echo = True


def get_session() -> Session:
    return Session(engine)


def get_async_session() -> AsyncSession:
    return AsyncSession(bind=async_engine)
