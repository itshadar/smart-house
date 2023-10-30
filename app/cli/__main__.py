import asyncio
from .cli_smart_house_builder import CLISmartHouseBuilder
from app.core.db_operations import get_async_uow


async def get_devices():
    async with get_async_uow() as uow:
        devices = await uow.electronic_devices.get_devices_metadata()
    return devices


def main():

    # using run_until_complete because lack of support in typer package
    # TODO: CONSIDER CHANGE TO CLICK/ASYNCCLICK
    loop = asyncio.get_event_loop()
    devices = loop.run_until_complete(get_devices())
    app = CLISmartHouseBuilder("smart house app").build(devices)
    app()


if __name__ == "__main__":
    main()
