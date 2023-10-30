from app.core.models import Microwave
from .electronic_device_repository import ElectronicDeviceSQLRepository


class MicrowaveSQLRepository(ElectronicDeviceSQLRepository):

    _model = Microwave

    async def get_degrees(self, device_id: int) -> int:
        statement = self._build_statement("degrees", id=device_id)
        return await self.get_scalar(statement)

    async def set_degrees_and_timer(self, device_id: int, degrees: int, timer: int):
        microwave = await self.get_by_id(device_id)
        microwave.degrees = degrees
        microwave.timer = timer
        await self.update(microwave)



