from typer import Argument, Context
from .electronic_device_command_set import ElectronicDeviceCommandSet
from src.core.utilities.constants import AirConditionerSettings
from src.cli.loggers import logger


class AirConditionerCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        async def set_degrees(ctx: Context,
                              degrees: int = Argument(...,
                                                      help="degrees value",
                                                      min=AirConditionerSettings.MIN_DEGREES,
                                                      max=AirConditionerSettings.MAX_DEGREES)):
            async with ctx.obj.async_uow as uow:
                await uow.air_conditioners.set_degrees(ctx.obj.device_id, degrees)
            logger.set_log(ctx.obj.device_name, "degrees", degrees)

        @self.app.command()
        async def get_degrees(ctx: Context):
            async with ctx.obj.async_uow as uow:
                degrees = await uow.air_conditioners.get_degrees(ctx.obj.device_id)
            logger.get_log(ctx.obj.device_name, "degrees", degrees)
