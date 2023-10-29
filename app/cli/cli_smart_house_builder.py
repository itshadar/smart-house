from typer import Typer
from app.core.utilities import DeviceType
from app.core.controllers import ControllerFactory
from .commands import DeviceCommandSetFactory


class SmartHouseAppBuilder:

    def __init__(self, app_name):
        self.app_name = app_name

    def build(self) -> Typer:
        app = Typer(name=self.app_name, help=f"Available Commands for {self.app_name}", no_args_is_help=True)
        controller = ControllerFactory.create(DeviceType.OTHER)
        devices = controller.get_all_devices_metadata()
        for device in devices:
            device_controller = ControllerFactory.create(device.type)
            device_app = self.build_device_app(device.name, device.id, device.type, device_controller)
            app.add_typer(device_app, name=device.name)
        return app

    @staticmethod
    def build_device_app(device_name, device_id, device_type, device_controller) -> Typer:
        device_app = Typer(name=device_name, help=f"Available commands for {device_name}", no_args_is_help=True)
        DeviceCommandSetFactory.setup(device_type, device_id, device_app, device_controller)
        return device_app
