import pytest
from sqlalchemy.sql import select
from app.core.models import Microwave
from app.core.utilities import DeviceStatus, DeviceType
from app.core.repositories import MicrowaveSQLRepository
from pytest_mock_resources import create_postgres_fixture


@pytest.fixture(scope='function')
def test_device():
    return Microwave(id=1, name="Test Microwave", status=DeviceStatus.OFF, degrees=30,
                     type=DeviceType.MICROWAVE, timer=0)


pg_session = create_postgres_fixture(Microwave, session=True, async_=True)


class TestTVSQLRepository:

    @pytest.mark.asyncio
    async def test_get_degrees(self, test_device, pg_session):
        pg_session.add(test_device)
        await pg_session.commit()

        repo = MicrowaveSQLRepository(pg_session)
        actual_degrees = await repo.get_degrees(device_id=1)
        excepted_degrees = 30

        assert actual_degrees == excepted_degrees

    @pytest.mark.asyncio
    async def test_set_degrees_and_timer(self, test_device, pg_session):
        pg_session.add(test_device)
        await pg_session.commit()

        repo = MicrowaveSQLRepository(pg_session)
        await repo.set_degrees_and_timer(device_id=1, degrees=28, timer=30)

        result = await pg_session.execute(select(Microwave).filter_by(id=1))
        updated_device = result.scalar()
        excepted_degrees = 28
        excepted_timer = 30
        assert updated_device.degrees == excepted_degrees
        assert updated_device.timer == excepted_timer
