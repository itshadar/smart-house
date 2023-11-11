import asyncio

from typer import Context

from src.cli.commands.command_set_factory import DeviceCommandSetFactory
from src.cli.utilities.async_typer import AsyncTyper
from src.core.db_operations import AsyncUnitOfWork, get_async_uow
from src.core.schemas import DeviceMetadata
from src.core.utilities.enums import DeviceType


class ContextDeviceAppObj:
    def __init__(self, async_uow, device_id: int, device_name: str, device_type: DeviceType):
        self.async_uow = async_uow
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type

    @property
    def repo(self):
        if self.device_type == DeviceType.MICROWAVE:
            return self.async_uow.microwaves
        elif self.device_type == DeviceType.TV:
            return self.async_uow.tvs
        elif self.device_type == DeviceType.AIRCONDITIONER:
            return self.async_uow.air_conditioners
        else:
            return self.async_uow.electronic_devices


def build_device_app(
    device_name: str,
    device_id: int,
    device_type: DeviceType,
    async_uow: AsyncUnitOfWork,
) -> AsyncTyper:
    def configure_device_driver(ctx: Context):
        ctx.obj = ContextDeviceAppObj(
            async_uow=async_uow, device_id=device_id, device_name=device_name, device_type=device_type
        )

    device_app = AsyncTyper(
        name=device_name,
        help=f"Available commands for {device_name}",
        no_args_is_help=True,
        callback=configure_device_driver,
    )
    DeviceCommandSetFactory.setup(device_type, device_app)
    return device_app


async def get_available_devices(async_uow: AsyncUnitOfWork) -> list[DeviceMetadata]:
    async with async_uow as uow:
        return await uow.electronic_devices.get_devices_metadata()


def build_app(async_uow: AsyncUnitOfWork):
    # I needed to make adaptions to support AsyncTyper and async commands within typer package and that why I used
    # loop.run_until_complete, although it's not best practice (should run the event_loop from main).
    # Click has extensions for async/await commands so maybe in the future I'll
    # replace typer package with click package.
    devices = asyncio.get_event_loop().run_until_complete(
        get_available_devices(async_uow)
    )
    app = AsyncTyper(
        name="Smart House",
        help="Available Commands for Smart House App",
        no_args_is_help=True,
    )
    for device in devices:
        device_app = build_device_app(device.name, device.id, device.type, async_uow)
        app.add_typer(device_app, name=device.name)
    return app
