import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.models import TV
from src.core.repositories.tv_repository import TVSQLRepository
from src.core.utilities.enums import DeviceStatus, DeviceType


@pytest.fixture(scope='function')
def test_device() -> TV:
    return TV(id=1, name="Test TV", status=DeviceStatus.OFF, channel=2, type=DeviceType.TV)


pg_session = create_postgres_fixture(TV, session=True, async_=True)


class TestTVSQLRepository:

    @pytest.mark.asyncio
    async def test_get_channel(self, test_device: TV, pg_session: AsyncSession) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo = TVSQLRepository(pg_session)
        actual_channel = await repo.get_channel(device_id=1)
        excepted_channel = 2

        assert actual_channel == excepted_channel

    @pytest.mark.asyncio
    async def test_set_channel(self, test_device: TV, pg_session: AsyncSession) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo = TVSQLRepository(pg_session)
        await repo.set_channel(device_id=1, channel=3)

        result = await pg_session.execute(select(TV).where(TV.id == 1))
        updated_device = result.scalar()
        excepted_channel = 3

        assert updated_device is not None, "Device not found"
        assert updated_device.channel == excepted_channel
