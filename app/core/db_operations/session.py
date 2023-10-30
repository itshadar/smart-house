from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_session, create_async_engine
from config import database_uri, async_database_uri


engine = create_engine(database_uri)
debug_engine = create_engine(database_uri, echo=True)

debug_async_engine = create_async_engine(async_database_uri, echo=True)
async_engine = create_async_engine(async_database_uri, echo=True)


def get_session() -> Session:
    return Session(engine)


def get_async_session() -> AsyncSession:
    return AsyncSession(bind=async_engine)
