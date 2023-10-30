from .base_command_set import BaseCommandSet
from typer import Argument, echo, Typer
from app.core.utilities import DeviceStatus
from app.core.db_operations import get_uow, get_async_uow
import anyio
import asyncio



class ElectronicDeviceCommandSet(BaseCommandSet):

    def __init__(self, app: Typer, device_id: int):
        super().__init__(app)
        self.device_id = device_id

    def echo_set_cmd(self, attr: str, attr_value: any):
        echo(f"Set {self.app.info.name} {attr} to {attr_value}")

    def echo_get_command(self, attr: str, attr_value: any):
        echo(f"{self.app.info.name} {attr} is {attr_value}")

    def commands(self):

        @self.app.command()
        async def get_status():
            async with get_async_uow() as uow:
                status: DeviceStatus = await uow.electronic_devices.get_status(self.device_id)
            self.echo_get_command("status", status.name)

        @self.app.command()
        async def set_status(status: DeviceStatus = Argument(default='OFF')):
            async with get_async_uow() as uow:
                await uow.electronic_devices.set_status(self.device_id, status)
            self.echo_set_cmd("status", status.name)
