from app.core.models import TV
from .electronic_device_repository import ElectronicDeviceSQLRepository


class TVSQLRepository(ElectronicDeviceSQLRepository):

    _model = TV

    async def get_channel(self, device_id: int):
        statement = self._build_statement("channel", id=device_id)
        return await self.get_scalar(statement)

    async def set_channel(self, device_id: int, channel: int):
        tv = await self.get_by_id(device_id)
        tv.channel = channel
        await self.update(tv)
