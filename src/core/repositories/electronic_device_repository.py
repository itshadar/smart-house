from abc import ABC, abstractmethod

from src.core.models import ElectronicDevice
from src.core.repositories.sql_repository import SQLRepository
from src.core.schemas import DeviceMetadata
from src.core.utilities.constants import DeviceStatus


class ElectronicDeviceBaseRepository(ABC):
    @abstractmethod
    async def get_devices_metadata(self, **filters) -> list[DeviceMetadata]:
        raise NotImplementedError()

    @abstractmethod
    async def get_status(self, device_id: int) -> DeviceStatus | None:
        raise NotImplementedError()

    @abstractmethod
    async def set_status(self, device_id: int, status: DeviceStatus) -> None:
        raise NotImplementedError()


class ElectronicDeviceSQLRepository(
    ElectronicDeviceBaseRepository, SQLRepository[ElectronicDevice]
):
    _model = ElectronicDevice

    def __init__(self, session):
        super().__init__(session, self._model)

    async def get_devices_metadata(self, **filters) -> list[DeviceMetadata]:
        statement = self._build_statement(*DeviceMetadata._fields, **filters)
        devices_metadata = await self.get_all(statement)
        return [DeviceMetadata(*device) for device in devices_metadata]

    async def get_status(self, device_id: int) -> DeviceStatus:
        return await self.get_col_by_id(col_name="status", id=device_id)

    async def set_status(self, device_id: int, status: DeviceStatus) -> None:
        device = await self.get_by_id(device_id)
        setattr(device, "status", status)
        await self.update(device)
