from typer import Argument, Context
from .electronic_device_command_set import ElectronicDeviceCommandSet
from app.core.utilities import MicrowaveSettings
from app.core.db_operations import get_async_uow
from app.cli.loggers import logger


class MicrowaveCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        async def set_degrees_and_timer(ctx: Context,
                                        degrees: int = Argument(help="degrees value",
                                                                min=MicrowaveSettings.MIN_DEGREES,
                                                                max=MicrowaveSettings.MAX_DEGREES),
                                        timer: int = Argument(help="timer value in seconds",
                                                              min=MicrowaveSettings.MIN_TIMER)):
            async with ctx.obj.async_uow as uow:
                await uow.microwaves.set_degrees_and_timer(ctx.obj.device_id, degrees, timer)
            logger.set_log(ctx.obj.device_name, "degrees", degrees)
            logger.set_log(ctx.obj.device_name, "timer", timer)

        @self.app.command()
        async def get_degrees(ctx: Context):
            async with ctx.obj.async_uow as uow:
                degrees = await uow.microwaves.get_degrees(ctx.obj.device_id)
            logger.get_log(ctx.obj.device_name, "degrees", degrees)

