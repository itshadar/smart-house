import asyncio
from typing import Callable

import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession
from typer.testing import CliRunner

from tests.test_cli.utilities import create_session_factory
from src.cli.configure_apps import build_app
from src.cli.utilities.async_typer import AsyncTyper
from src.core.db_operations import AsyncUnitOfWork
from src.core.models import (TV, AirConditioner, Base, ElectronicDevice,
                             Microwave)
from src.core.utilities.enums import DeviceType

async_pg_session = create_postgres_fixture(Base, session=True, async_=True)


@pytest.fixture()
def app() -> AsyncTyper:
    app = AsyncTyper(name="Smart House", help="Available Commands for Smart House App", no_args_is_help=True)
    return app


@pytest.fixture()
def async_session_factory(async_pg_session: AsyncSession) -> Callable[[], AsyncSession]:
    return create_session_factory(async_pg_session)


@pytest.fixture()
def mock_async_uow(async_session_factory: Callable[[], AsyncSession]) -> AsyncUnitOfWork:
    return AsyncUnitOfWork(async_session_factory)


class TestElectronicDeviceApp:

    def test_list_command(self, mock_async_uow: AsyncUnitOfWork, async_pg_session: AsyncSession) -> None:
        async_pg_session.add_all(instances=[ElectronicDevice(id=1, name="Test Device"),
                                            Microwave(id=2, name="Test Microwave", type=DeviceType.MICROWAVE),
                                            Microwave(id=3, name="Test Microwave2", type=DeviceType.MICROWAVE),
                                            TV(id=4, name="Test TV", type=DeviceType.TV),
                                            AirConditioner(id=5, name="Test AC", type=DeviceType.AIRCONDITIONER)])

        asyncio.get_event_loop().run_until_complete(async_pg_session.commit())

        test_app = build_app(mock_async_uow)

        runner = CliRunner()
        result = runner.invoke(test_app, ["--help"])
        assert result.exit_code == 0
        assert "Test Device" in result.output
        assert "Test Microwave" in result.output
        assert "Test Microwave2" in result.output
        assert "Test TV" in result.output
        assert "Test AC" in result.output
