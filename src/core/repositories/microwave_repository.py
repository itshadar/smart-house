from abc import ABC, abstractmethod

from src.core.models import Microwave
from src.core.repositories.electronic_device_repository import (
    ElectronicDeviceBaseRepository,
    ElectronicDeviceSQLRepository,
)
from src.core.schemas import MicrowaveSchema


class MicrowaveBaseRepository(ElectronicDeviceBaseRepository, ABC):
    @abstractmethod
    async def get_degrees(self, device_id: int) -> int | None:
        ...

    @abstractmethod
    async def set_degrees_and_timer(
        self, device_id: int, degrees: int, timer: int
    ) -> None:
        ...


class MicrowaveSQLRepository(
    MicrowaveBaseRepository, ElectronicDeviceSQLRepository[Microwave, MicrowaveSchema]
):
    _model = Microwave

    async def get_degrees(self, device_id: int) -> int | None:
        return await self.get_col_by_id(col_name="degrees", record_id=device_id)

    async def set_degrees_and_timer(
        self, device_id: int, degrees: int, timer: int
    ) -> None:
        microwave = await self.get_by_id(device_id)
        setattr(microwave, "degrees", degrees)
        setattr(microwave, "timer", timer)
        await self.update(microwave)
