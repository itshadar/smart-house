from typer import Argument
from .electronic_device_command_set import ElectronicDeviceCommandSet
from app.core.utilities import AirConditionerSettings
from app.core.db_operations import get_async_uow


class AirConditionerCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        async def set_degrees(degrees: int = Argument(..., help="degrees value",
                              min=AirConditionerSettings.MIN_DEGREES,
                              max=AirConditionerSettings.MAX_DEGREES)):

            async with get_async_uow() as uow:
                await uow.air_conditioners.set_degrees(self.device_id, degrees)
            self.echo_set_cmd("degrees", degrees)

        @self.app.command()
        async def get_degrees():
            async with get_async_uow() as uow:
                degrees = await uow.air_conditioners.get_degrees(self.device_id)
            self.echo_get_command("degrees", degrees)

