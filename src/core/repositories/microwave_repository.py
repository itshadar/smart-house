from abc import ABC, abstractmethod
from src.core.models import Microwave
from .electronic_device_repository import ElectronicDeviceSQLRepository, ElectronicDeviceBaseRepository


class MicrowaveBaseRepository(ElectronicDeviceBaseRepository, ABC):

    @abstractmethod
    def get_degrees(self, device_id: int) -> int | None:
        raise NotImplementedError()

    @abstractmethod
    def set_degrees_and_timer(self, device_id: int, degrees: int, timer: int) -> None:
        raise NotImplementedError()


class MicrowaveSQLRepository(MicrowaveBaseRepository, ElectronicDeviceSQLRepository):

    _model = Microwave

    async def get_degrees(self, device_id: int) -> int | None:
        statement = self._build_statement("degrees", id=device_id)
        return await self.get_scalar(statement)

    async def set_degrees_and_timer(self, device_id: int, degrees: int, timer: int) -> None:
        microwave = await self.get_by_id(device_id)
        if microwave:
            microwave.degrees = degrees
            microwave.timer = timer
            await self.update(microwave)
