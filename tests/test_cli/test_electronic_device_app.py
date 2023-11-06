import asyncio
from typing import Callable

import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession
from typer.testing import CliRunner

from src.cli.configure_apps import build_device_app
from src.cli.utilities.async_typer import AsyncTyper
from src.core.db_operations import AsyncUnitOfWork
from src.core.models import ElectronicDevice
from src.core.utilities.enums import DeviceStatus, DeviceType

async_pg_session = create_postgres_fixture(ElectronicDevice, session=True, async_=True)


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
    test_device = ElectronicDevice(id=1, name="Test", status=DeviceStatus.OFF)
    async_pg_session.add(test_device)
    asyncio.get_event_loop().run_until_complete(async_pg_session.commit())
    return build_device_app(device_name="Test", device_id=1, device_type=DeviceType.OTHER,
                            async_uow=mock_async_uow)


class TestElectronicDeviceApp:

    def test_set_status_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app, args=["set-status", "ON"])
        assert result.exit_code == 0
        assert "ON" in result.output

    def test_set_status_validation_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app, args=["set-status", "TestStatus"])
        assert "Invalid value for '[STATUS]" in result.output
        assert result.exit_code != 0

    def test_get_status_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app, ["get-status"])
        assert result.exit_code == 0
        assert "OFF" in result.output

    def test_list_command(self, test_device_app: AsyncTyper):
        runner = CliRunner()
        result = runner.invoke(test_device_app, ["--help"])
        assert result.exit_code == 0
        assert "get-status" in result.output
        assert "set-status" in result.output
