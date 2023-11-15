from typing import Callable

import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession
from typer.testing import CliRunner

from src.cli.utilities.async_typer import AsyncTyper
from src.core.db_operations import AsyncUnitOfWork
from src.core.models import Microwave
from src.core.utilities.constants import MicrowaveSettings
from src.core.utilities.enums import DeviceType
from tests.test_cli.utilities import create_device_app, create_session_factory

async_pg_session = create_postgres_fixture(Microwave, session=True, async_=True)


@pytest.fixture()
def async_session_factory(async_pg_session: AsyncSession) -> Callable[[], AsyncSession]:
    return create_session_factory(async_pg_session)


@pytest.fixture()
def mock_async_uow(
    async_session_factory: Callable[[], AsyncSession]
) -> AsyncUnitOfWork:
    return AsyncUnitOfWork(async_session_factory)


@pytest.fixture()
def test_device_app(
    mock_async_uow: AsyncUnitOfWork, async_pg_session: AsyncSession
) -> AsyncTyper:
    test_device = Microwave(id=1, name="Test", degrees=27, type=DeviceType.MICROWAVE)
    return create_device_app(
        async_uow=mock_async_uow, async_pg_session=async_pg_session, device=test_device
    )


class TestElectronicDeviceApp:
    def test_set_degrees_and_timer_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(
            test_device_app, args=["set-degrees-and-timer", "25", "30"]
        )
        assert result.exit_code == 0
        assert "[INFO] Set Test degrees to 25" in result.output
        assert "[INFO] Set Test timer to 30" in result.output

    def test_set_degrees_and_timer_validation_command(
        self, test_device_app: AsyncTyper
    ) -> None:
        runner = CliRunner()

        result = runner.invoke(
            test_device_app, args=["set-degrees-and-timer", "test", "30"]
        )
        assert (
            "Invalid value for 'DEGREES': 'test' is not a valid integer range."
            in result.output
        )
        assert result.exit_code != 0

        result = runner.invoke(
            test_device_app, args=["set-degrees-and-timer", "25", "test"]
        )
        assert (
            "Invalid value for 'TIMER': 'test' is not a valid integer range."
            in result.output
        )
        assert result.exit_code != 0

        result = runner.invoke(
            test_device_app, args=["set-degrees-and-timer", "0", "30"]
        )
        assert (
            f"Invalid value for 'DEGREES': 0 is not in the range "
            f"{MicrowaveSettings.MIN_DEGREES}<=x<={MicrowaveSettings.MAX_DEGREES}."
            in result.output
        )
        assert result.exit_code != 0

        result = runner.invoke(
            test_device_app, args=["set-degrees-and-timer", "40", "30"]
        )
        assert (
            f"Invalid value for 'DEGREES': 40 is not in the range "
            f"{MicrowaveSettings.MIN_DEGREES}<=x<={MicrowaveSettings.MAX_DEGREES}."
            in result.output
        )
        assert result.exit_code != 0

    def test_get_degrees_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(test_device_app, ["get-degrees"])
        assert result.exit_code == 0
        assert "[INFO] Test degrees is 27" in result.output

    def test_list_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(test_device_app)
        assert result.exit_code == 0
        assert "get-degrees" in result.output
        assert "set-status" in result.output
        assert "set-degrees-and-timer" in result.output
        assert "get-status" in result.output
