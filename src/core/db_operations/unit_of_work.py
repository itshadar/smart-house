from typing import Callable, Any
from typing_extensions import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.air_conditioner_repository import AirConditionerSQLRepository
from src.core.repositories.electronic_device_repository import (
    ElectronicDeviceSQLRepository,
)
from src.core.repositories.microwave_repository import MicrowaveSQLRepository
from src.core.repositories.tv_repository import TVSQLRepository
from src.core.schemas import ElectronicDeviceSchema
from src.core.models import ElectronicDevice


from .session import get_async_session


class AsyncUnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession
        self.electronic_devices: ElectronicDeviceSQLRepository[
            ElectronicDevice, ElectronicDeviceSchema
        ]
        self.tvs: TVSQLRepository
        self.microwaves: MicrowaveSQLRepository
        self.air_conditioners: AirConditionerSQLRepository

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self.electronic_devices = ElectronicDeviceSQLRepository(self._session)
        self.tvs = TVSQLRepository(self._session)
        self.microwaves = MicrowaveSQLRepository(self._session)
        self.air_conditioners = AirConditionerSQLRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close(self) -> None:
        await self._session.close()


def get_async_uow() -> AsyncUnitOfWork:
    return AsyncUnitOfWork(get_async_session)
