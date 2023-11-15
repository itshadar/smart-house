from typing import Callable

import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession
from typer.testing import CliRunner

from tests.test_cli.utilities import create_session_factory, create_device_app
from src.cli.utilities.async_typer import AsyncTyper
from src.core.db_operations import AsyncUnitOfWork
from src.core.models import AirConditioner
from src.core.utilities.constants import AirConditionerSettings
from src.core.utilities.enums import DeviceType

async_pg_session = create_postgres_fixture(AirConditioner, session=True, async_=True)


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
    test_device = AirConditioner(
        id=1, name="Test", degrees=15, type=DeviceType.AIRCONDITIONER
    )
    return create_device_app(
        async_uow=mock_async_uow, async_pg_session=async_pg_session, device=test_device
    )


class TestElectronicDeviceApp:
    def test_set_degrees_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(test_device_app, args=["set-degrees", "20"])
        assert result.exit_code == 0
        assert "[INFO] Set Test degrees to 20" in result.output

    def test_set_degrees_validation_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(test_device_app, args=["set-degrees", "test"])
        assert (
            "Invalid value for 'DEGREES': 'test' is not a valid integer range."
            in result.output
        )
        assert result.exit_code != 0

        result = runner.invoke(test_device_app, args=["set-degrees", "0"])
        assert (
            f"Invalid value for 'DEGREES': 0 is not in the range "
            f"{AirConditionerSettings.MIN_DEGREES}<=x<={AirConditionerSettings.MAX_DEGREES}."
            in result.output
        )
        assert result.exit_code != 0

        result = runner.invoke(test_device_app, args=["set-degrees", "40"])
        assert (
            f"Invalid value for 'DEGREES': 40 is not in the range "
            f"{AirConditionerSettings.MIN_DEGREES}<=x<={AirConditionerSettings.MAX_DEGREES}."
            in result.output
        )
        assert result.exit_code != 0

    def test_get_degrees_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(test_device_app, ["get-degrees"])
        assert result.exit_code == 0
        assert "[INFO] Test degrees is 15" in result.output

    def test_list_command(self, test_device_app: AsyncTyper) -> None:
        runner = CliRunner()
        result = runner.invoke(test_device_app)
        assert result.exit_code == 0
        assert "get-degrees" in result.output
        assert "set-status" in result.output
        assert "set-degrees" in result.output
        assert "get-status" in result.output
