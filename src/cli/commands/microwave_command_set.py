from typer import Argument, Context

from src.cli.commands.electronic_device_command_set import \
    ElectronicDeviceCommandSet
from src.cli.loggers import logger
from src.core.utilities.constants import MicrowaveSettings


class MicrowaveCommandSet(ElectronicDeviceCommandSet):
    def commands(self):
        super().commands()

        @self.app.command()
        async def set_degrees_and_timer(
            ctx: Context,
            degrees: int = Argument(
                help="degrees value",
                min=MicrowaveSettings.MIN_DEGREES,
                max=MicrowaveSettings.MAX_DEGREES,
            ),
            timer: int = Argument(
                help="timer value in seconds", min=MicrowaveSettings.MIN_TIMER
            ),
        ):
            async with ctx.obj.async_uow:
                await ctx.obj.repo.set_degrees_and_timer(
                    ctx.obj.device_id, degrees, timer
                )
            logger.set_log(ctx.obj.device_name, "degrees", degrees)
            logger.set_log(ctx.obj.device_name, "timer", timer)

        @self.app.command()
        async def get_degrees(ctx: Context):
            async with ctx.obj.async_uow:
                degrees = await ctx.obj.repo.get_degrees(ctx.obj.device_id)
            logger.get_log(ctx.obj.device_name, "degrees", degrees)
