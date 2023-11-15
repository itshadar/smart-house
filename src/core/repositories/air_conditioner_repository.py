from abc import ABC, abstractmethod

from src.core.models import AirConditioner
from src.core.schemas import AirConditionerSchema
from src.core.repositories.electronic_device_repository import (
    ElectronicDeviceBaseRepository, ElectronicDeviceSQLRepository)


class AirConditionerBaseRepository(ElectronicDeviceBaseRepository, ABC):
    @abstractmethod
    async def get_degrees(self, device_id: int) -> int:
        ...

    @abstractmethod
    async def set_degrees(self, device_id: int, degrees: int) -> None:
        ...


class AirConditionerSQLRepository(
    AirConditionerBaseRepository, ElectronicDeviceSQLRepository[AirConditioner, AirConditionerSchema]
):
    _model = AirConditioner

    async def get_degrees(self, device_id: int) -> int:
        return await self.get_col_by_id(col_name="degrees", record_id=device_id)

    async def set_degrees(self, device_id: int, degrees: int) -> None:
        ac = await self.get_by_id(device_id)
        setattr(ac, "degrees", degrees)
        await self.update(ac)
