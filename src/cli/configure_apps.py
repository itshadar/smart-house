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
    # Adaptations were made to support AsyncTyper and asynchronous commands within the Typer package.
    # This required using loop.run_until_complete, though ideally, the event loop should be run from main.
    # Reference: https://github.com/tiangolo/typer/issues/88
    # Future Consideration: Transitioning to the Click package, which natively supports async/await, might be explored.

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
