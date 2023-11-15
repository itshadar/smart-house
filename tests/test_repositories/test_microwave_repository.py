import pytest
from typing import Type
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Microwave
from src.core.repositories.microwave_repository import MicrowaveSQLRepository
from src.core.utilities.enums import DeviceStatus, DeviceType


@pytest.fixture(scope='function')
def test_device() -> Microwave:
    return Microwave(id=1, name="Test Microwave", status=DeviceStatus.OFF, degrees=30,
                     type=DeviceType.MICROWAVE, timer=0)


pg_session = create_postgres_fixture(Microwave, session=True, async_=True)


class TestTVSQLRepository:

    @pytest.mark.asyncio
    async def test_get_degrees(self, test_device: Microwave, pg_session: AsyncSession) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo = MicrowaveSQLRepository(pg_session)
        actual_degrees = await repo.get_degrees(device_id=1)
        excepted_degrees = 30

        assert actual_degrees == excepted_degrees

    @pytest.mark.asyncio
    async def test_set_degrees_and_timer(self, test_device: Microwave, pg_session: AsyncSession) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo = MicrowaveSQLRepository(pg_session)
        await repo.set_degrees_and_timer(device_id=1, degrees=28, timer=30)

        updated_device: Type[Microwave] | None = await pg_session.get_one(Microwave, 1)

        excepted_degrees = 28
        excepted_timer = 30

        assert updated_device is not None, "Device not found"
        assert updated_device.degrees == excepted_degrees
        assert updated_device.timer == excepted_timer
