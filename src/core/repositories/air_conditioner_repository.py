from app.core.models import AirConditioner
from .electronic_device_repository import ElectronicDeviceSQLRepository


class AirConditionerSQLRepository(ElectronicDeviceSQLRepository):

    _model = AirConditioner

    async def get_degrees(self, device_id: int) -> int:
        statement = self._build_statement("degrees", id=device_id)
        return await self.get_scalar(statement)

    async def set_degrees(self, device_id: int, degrees: int):
        ac = await self.get_by_id(device_id)
        ac.degrees = degrees
        await self.update(ac)

