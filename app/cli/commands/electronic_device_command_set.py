from .base_command_set import BaseCommandSet
from typer import Argument, Context
from app.core.utilities import DeviceStatus
from app.cli.loggers import logger
from app.cli.utilities.async_typer import AsyncTyper


class ElectronicDeviceCommandSet(BaseCommandSet):

    def __init__(self, app: AsyncTyper):
        super().__init__(app)

    def commands(self):

        @self.app.command()
        async def get_status(ctx: Context):
            async with ctx.obj.async_uow as uow:
                status: DeviceStatus = await uow.electronic_devices.get_status(ctx.obj.device_id)
            logger.get_log(ctx.obj.device_name, "status", status.name)

        @self.app.command()
        async def set_status(ctx: Context, status: DeviceStatus = Argument(default='OFF')):
            async with ctx.obj.async_uow as uow:
                await uow.electronic_devices.set_status(ctx.obj.device_id, status)
            logger.set_log(ctx.obj.device_name, "status", status.name)
