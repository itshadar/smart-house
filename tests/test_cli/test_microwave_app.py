import asyncio
from typing import Callable

import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession
from typer.testing import CliRunner

from src.cli.configure_apps import build_device_app
from src.cli.utilities.async_typer import AsyncTyper
from src.core.db_operations import AsyncUnitOfWork
from src.core.models import Microwave
from src.core.utilities.constants import MicrowaveSettings
from src.core.utilities.enums import DeviceType

async_pg_session = create_postgres_fixture(Microwave, session=True, async_=True)


def create_session_factory(async_session):
    def session_factory():
        return async_session
    return session_factory


@pytest.fixture()
def async_session_factory(async_pg_session) -> Callable[[], AsyncSession]:
    return create_session_factory(async_pg_session)


@pytest.fixture()
def mock_async_uow(async_session_factory: Callable[[], AsyncSession]) -> AsyncUnitOfWork:
    return AsyncUnitOfWork(async_session_factory)


@pytest.fixture()
def test_device_app(mock_async_uow: AsyncUnitOfWork, async_pg_session: AsyncSession):
    test_device = Microwave(id=1, name="Test", degrees=27, type=DeviceType.MICROWAVE)
    async_pg_session.add(test_device)
    asyncio.get_event_loop().run_until_complete(async_pg_session.commit())
    return build_device_app(device_name="Test", device_id=1, device_type=DeviceType.MICROWAVE,
                            async_uow=mock_async_uow)


class TestElectronicDeviceApp:

    def test_set_degrees_and_timer_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app, args=["set-degrees-and-timer", "25", "30"])
        assert result.exit_code == 0
        assert "25" in result.output
        assert "30" in result.output

    def test_set_degrees_and_timer_validation_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()

        result = runner.invoke(test_device_app, args=["set-degrees-and-timer", "test", "30"])
        assert "Invalid value for 'DEGREES': 'test' is not a valid integer range." in result.output
        assert result.exit_code != 0

        result = runner.invoke(test_device_app, args=["set-degrees-and-timer", "25", "test"])
        assert "Invalid value for 'TIMER': 'test' is not a valid integer range." in result.output
        assert result.exit_code != 0

        result = runner.invoke(test_device_app, args=["set-degrees-and-timer", "0", "30"])
        assert f"Invalid value for 'DEGREES': 0 is not in the range " \
               f"{MicrowaveSettings.MIN_DEGREES}<=x<={MicrowaveSettings.MAX_DEGREES}." in result.output
        assert result.exit_code != 0

        result = runner.invoke(test_device_app, args=["set-degrees-and-timer", "40", "30"])
        assert f"Invalid value for 'DEGREES': 40 is not in the range " \
               f"{MicrowaveSettings.MIN_DEGREES}<=x<={MicrowaveSettings.MAX_DEGREES}." in result.output
        assert result.exit_code != 0

    def test_get_degrees_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app, ["get-degrees"])
        assert result.exit_code == 0
        assert "27" in result.output

    def test_list_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app)
        assert result.exit_code == 0
        assert "get-degrees" in result.output
        assert "set-status" in result.output
        assert "set-degrees-and-timer" in result.output
        assert "get-status" in result.output
