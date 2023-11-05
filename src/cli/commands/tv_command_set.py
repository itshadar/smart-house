from typer import Argument, Context
from .electronic_device_command_set import ElectronicDeviceCommandSet
from app.core.utilities import TVSettings
from app.core.db_operations import get_async_uow
from app.cli.loggers import logger


class TVCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        async def switch_channel(ctx: Context,
                                 channel: int = Argument(..., help="channel value",
                                                         min=TVSettings.MIN_CHANNEL,
                                                         max=TVSettings.MAX_CHANNEL)):
            async with ctx.obj.async_uow as uow:
                await uow.tvs.set_channel(ctx.obj.device_id, channel)
            logger.set_log(ctx.obj.device_name, "channel", channel)

        @self.app.command()
        async def get_channel(ctx: Context):
            async with ctx.obj.async_uow as uow:
                channel = await uow.tvs.get_channel(ctx.obj.device_id)
            logger.get_log(ctx.obj.device_name, "channel", channel)
