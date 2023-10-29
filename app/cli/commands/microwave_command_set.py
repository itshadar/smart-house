from typer import Argument, Context
from .electronic_device_command_set import ElectronicDeviceCommandSet
from constants import MicrowaveSettings


class MicrowaveCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        def set_degrees_and_timer(ctx: Context,
                                  degrees: int = Argument(help="degrees value",
                                                          min=MicrowaveSettings.MIN_DEGREES,
                                                          max=MicrowaveSettings.MAX_DEGREES),
                                  timer: int = Argument(help="timer value in seconds",
                                                        min=MicrowaveSettings.MIN_TIMER)):
            self.controller.set_degrees_and_timer(self.device_id, degrees, timer)
            self.set_log("degrees", degrees)
            self.set_log("timer", timer)

        @self.app.command()
        def get_degrees(ctx: Context):

            degrees = self.controller.get_degrees(self.device_id)
            self.get_log("degrees", degrees)

