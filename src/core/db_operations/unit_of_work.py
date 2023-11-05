from app.core.repositories import ElectronicDeviceSQLRepository, MicrowaveSQLRepository, TVSQLRepository, AirConditionerSQLRepository
from abc import ABC, abstractmethod
from typing import Callable, Union
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .session import get_session, get_async_session


class UnitOfWorkBase(ABC):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            self.rollback()
            raise exc_val
        else:
            self.commit()
        self.close()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()


class AsyncUnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession = None
        self.electronic_devices = None
        self.tvs = None
        self.microwaves = None
        self.air_conditioners = None

    async def __aenter__(self):
        self._session = self._session_factory()
        self.electronic_devices = ElectronicDeviceSQLRepository(self._session)
        self.tvs = TVSQLRepository(self._session)
        self.microwaves = MicrowaveSQLRepository(self._session)
        self.air_conditioners = AirConditionerSQLRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
            raise exc_val
        else:
            await self.commit()
        await self.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()
        self._session = None


def get_async_uow():
    return AsyncUnitOfWork(get_async_session)

