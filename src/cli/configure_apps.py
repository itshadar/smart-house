import asyncio
from typer import Context
from .commands import DeviceCommandSetFactory
from app.cli.utilities.async_typer import AsyncTyper
from app.core.utilities import DeviceType
from app.core.schemas import DeviceMetadata
from app.core.db_operations import AsyncUnitOfWork


class ContextDeviceAppObj:
    def __init__(self, async_uow: AsyncUnitOfWork, device_id, device_name):
        self.async_uow = async_uow
        self.device_id = device_id
        self.device_name = device_name


def build_device_app(device_name: str, device_id: int, device_type: DeviceType, async_uow: AsyncUnitOfWork) -> AsyncTyper:

    def configure_device_driver(ctx: Context):
        ctx.obj = ContextDeviceAppObj(async_uow=async_uow, device_id=device_id, device_name=device_name)

    device_app = AsyncTyper(
        name=device_name,
        help=f"Available commands for {device_name}",
        no_args_is_help=True,
        callback=configure_device_driver
    )
    DeviceCommandSetFactory.setup(device_type, device_app)
    return device_app


async def get_available_devices(async_uow: AsyncUnitOfWork) -> list[DeviceMetadata]:
    async with async_uow as uow:
        return await uow.electronic_devices.get_devices_metadata()


def build_app(async_uow: AsyncUnitOfWork):
    devices = asyncio.get_event_loop().run_until_complete(get_available_devices(async_uow))
    app = AsyncTyper(name="Smart House", help=f"Available Commands for Smart House App", no_args_is_help=True)
    for device in devices:
        device_app = build_device_app(device.name, device.id, device.type, async_uow)
        app.add_typer(device_app, name=device.name)
    return app
