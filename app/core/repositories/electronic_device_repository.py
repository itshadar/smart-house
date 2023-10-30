from app.core.models import ElectronicDevice
from app.core.schemas import DeviceMetadata
from .sql_repository import SQLRepository
from app.core.utilities import DeviceStatus
#from app.core.db_operations import get_async_uow
import anyio

from sqlalchemy import select, text


class ElectronicDeviceSQLRepository(SQLRepository):

    _model = ElectronicDevice

    def __init__(self, session):
        super().__init__(session, self._model)

    async def get_devices_metadata(self, **filters) -> list[tuple]:
        statement = self._build_statement(*DeviceMetadata._fields, **filters)
        return await self.get_all(statement)

    async def get_status(self, device_id: int) -> DeviceStatus:
        statement = self._build_statement("status", id=device_id)
        return await self.get_scalar(statement)

    async def set_status(self, device_id: int, status: DeviceStatus):
        device = await self.get_by_id(device_id)
        device.status = status
        await self.update(device)

