from abc import ABC, abstractmethod
from src.core.models import AirConditioner
from .electronic_device_repository import ElectronicDeviceSQLRepository, ElectronicDeviceBaseRepository


class AirConditionerBaseRepository(ElectronicDeviceBaseRepository, ABC):

    @abstractmethod
    def get_degrees(self, device_id: int) -> int | None:
        raise NotImplementedError()

    @abstractmethod
    def set_degrees(self, device_id: int, degrees: int):
        raise NotImplementedError()


class AirConditionerSQLRepository(AirConditionerBaseRepository, ElectronicDeviceSQLRepository):

    _model = AirConditioner

    async def get_degrees(self, device_id: int) -> int | None:
        statement = self._build_statement("degrees", id=device_id)
        return await self.get_scalar(statement)

    async def set_degrees(self, device_id: int, degrees: int):
        ac = await self.get_by_id(device_id)
        if ac:
            ac.degrees = degrees
            await self.update(ac)

