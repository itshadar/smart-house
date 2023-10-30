from typer import Typer
from .commands import DeviceCommandSetFactory
from .async_typer import AsyncTyper
from app.core.schemas import DeviceMetadata
from app.core.utilities import DeviceType


class CLISmartHouseBuilder:

    def __init__(self, app_name: str):
        self.app_name = app_name

    def build(self, devices: list[DeviceMetadata]) -> Typer:
        app = Typer(name=self.app_name, help=f"Available Commands for {self.app_name}", no_args_is_help=True)
        for device in devices:
            device_app = self.build_device_app(device.name, device.id, device.type)
            app.add_typer(device_app, name=device.name)
        return app

    @staticmethod
    def build_device_app(device_name: str, device_id: int, device_type: DeviceType) -> Typer:
        device_app = AsyncTyper(name=device_name, help=f"Available commands for {device_name}", no_args_is_help=True)
        DeviceCommandSetFactory.setup(device_type, device_id, device_app)
        return device_app
