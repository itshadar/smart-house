from typer import Argument
from .electronic_device_command_set import ElectronicDeviceCommandSet
from app.core.utilities import MicrowaveSettings
from app.core.db_operations import get_async_uow


class MicrowaveCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        async def set_degrees_and_timer(degrees: int = Argument(help="degrees value",
                                                                min=MicrowaveSettings.MIN_DEGREES,
                                                                max=MicrowaveSettings.MAX_DEGREES),
                                        timer: int = Argument(help="timer value in seconds",
                                                              min=MicrowaveSettings.MIN_TIMER)):
            async with get_async_uow() as uow:
                await uow.microwaves.set_degrees_and_timer(self.device_id, degrees, timer)
            self.echo_set_cmd("degrees", degrees)
            self.echo_set_cmd("timer", timer)

        @self.app.command()
        async def get_degrees():
            async with get_async_uow() as uow:
                degrees = await uow.microwaves.get_degrees(self.device_id)
            self.echo_get_command("degrees", degrees)

