from typer import Argument
from .electronic_device_command_set import ElectronicDeviceCommandSet
from app.core.utilities import TVSettings
from app.core.db_operations import get_async_uow


class TVCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        async def switch_channel(channel: int = Argument(..., help="channel value",
                                                         min=TVSettings.MIN_CHANNEL)):
            async with get_async_uow() as uow:
                await uow.tvs.set_channel(self.device_id, channel)
            self.echo_set_cmd("channel", channel)

        @self.app.command()
        async def get_channel():
            async with get_async_uow() as uow:
                channel = await uow.tvs.get(self.device_id)
            self.echo_get_command("channel", channel)
