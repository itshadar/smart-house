from typer import Argument, Context
from .electronic_device_command_set import ElectronicDeviceCommandSet
from constants import AirConditionerSettings


class AirConditionerCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        def set_degrees(ctx: Context,
                        degrees: int = Argument(..., help="degrees value",
                                                min=AirConditionerSettings.MIN_DEGREES,
                                                max=AirConditionerSettings.MAX_DEGREES
                                                )):
            self.controller.set_degrees(self.device_id, degrees)
            self.set_log("degrees", degrees)

        @self.app.command()
        def get_degrees(ctx: Context):
            degrees = self.controller.get_degrees(self.device_id)
            self.get_log("degrees", degrees)

