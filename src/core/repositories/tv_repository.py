from abc import ABC, abstractmethod

from src.core.models import TV
from src.core.repositories.electronic_device_repository import (
    ElectronicDeviceBaseRepository, ElectronicDeviceSQLRepository)


class TVBaseRepository(ElectronicDeviceBaseRepository, ABC):
    @abstractmethod
    async def get_channel(self, device_id: int) -> int | None:
        raise NotImplementedError()

    @abstractmethod
    async def set_channel(self, device_id: int, channel: int) -> None:
        raise NotImplementedError()


class TVSQLRepository(TVBaseRepository, ElectronicDeviceSQLRepository):
    _model = TV

    async def get_channel(self, device_id: int) -> int | None:
        return await self.get_col_by_id(col_name="channel", id=device_id)

    async def set_channel(self, device_id: int, channel: int) -> None:
        tv = await self.get_by_id(device_id)
        setattr(tv, "channel", channel)
        await self.update(tv)
