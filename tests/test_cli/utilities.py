import asyncio

from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_operations import AsyncUnitOfWork
from src.core.models import ElectronicDevice
from src.core.utilities.enums import DeviceType
from src.cli.utilities.async_typer import AsyncTyper
from src.cli.configure_apps import build_device_app


def create_session_factory(async_session: AsyncSession) -> Callable[[], AsyncSession]:
    def session_factory() -> AsyncSession:
        return async_session
    return session_factory


def create_device_app(async_uow: AsyncUnitOfWork, async_pg_session: AsyncSession, device: ElectronicDevice) -> AsyncTyper:
    # Adaptations were made to support AsyncTyper and asynchronous commands within the Typer package.
    # This required using loop.run_until_complete, though ideally, the event loop should be run from main.
    # Reference: https://github.com/tiangolo/typer/issues/88

    async_pg_session.add(device)
    asyncio.get_event_loop().run_until_complete(async_pg_session.commit())
    return build_device_app(device_name=device.name, device_id=device.id, device_type=DeviceType(device.type),
                            async_uow=async_uow)
