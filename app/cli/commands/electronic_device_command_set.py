from .base_command_set import BaseCommandSet
from typer import Argument, echo, Context, Typer
import time
from constants import DeviceStatus


class ElectronicDeviceCommandSet(BaseCommandSet):

    def __init__(self, app, controller, device_id):
        super().__init__(app, controller)
        self.device_id = device_id

    def set_log(self, attr, attr_value):
        echo(f"Set {self.app.info.name} {attr} to {attr_value}")

    def get_log(self, attr, attr_value):
        echo(f"{self.app.info.name} {attr} is {attr_value}")

    @staticmethod
    def error_log(err, command=None):
        echo(err, err=True)

    def commands(self):

        @self.app.command()
        def get_status(ctx: Context):
            status: DeviceStatus = self.controller.get_status(self.device_id)
            self.get_log("status", status.name)

        @self.app.command()
        def set_status(ctx: Context, status: DeviceStatus = Argument(default='OFF')):
            self.controller.set_status(self.device_id, status)
            self.set_log("status", status.name)
