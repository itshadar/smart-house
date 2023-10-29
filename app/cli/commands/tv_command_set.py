from typer import Argument, Context
from .electronic_device_command_set import ElectronicDeviceCommandSet
from constants import TVSettings


class TVCommandSet(ElectronicDeviceCommandSet):

    def commands(self):
        super().commands()

        @self.app.command()
        def switch_channel(ctx: Context,
                           channel: int = Argument(...,
                                                   help="channel value",
                                                   min=TVSettings.MIN_CHANNEL)):

            self.controller.switch_channel(self.device_id, channel)
            self.set_log("channel", channel)

        @self.app.command()
        def get_channel(ctx: Context):
            channel = self.controller.get_channel(self.device_id)
            self.get_log("channel", channel)

