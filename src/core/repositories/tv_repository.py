from abc import ABC, abstractmethod

from src.core.models import TV
from src.core.schemas import TVSchema
from src.core.repositories.electronic_device_repository import (
    ElectronicDeviceBaseRepository,
    ElectronicDeviceSQLRepository,
)


class TVBaseRepository(ElectronicDeviceBaseRepository, ABC):
    @abstractmethod
    async def get_channel(self, device_id: int) -> int | None:
        ...

    @abstractmethod
    async def set_channel(self, device_id: int, channel: int) -> None:
        ...


class TVSQLRepository(TVBaseRepository, ElectronicDeviceSQLRepository[TV, TVSchema]):
    _model = TV

    async def get_channel(self, device_id: int) -> int | None:
        return await self.get_col_by_id(col_name="channel", record_id=device_id)

    async def set_channel(self, device_id: int, channel: int) -> None:
        tv = await self.get_by_id(device_id)
        setattr(tv, "channel", channel)
        await self.update(tv)
