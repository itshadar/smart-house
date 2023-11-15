import pytest
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from typing import Type
from src.core.models import AirConditioner
from src.core.repositories.air_conditioner_repository import AirConditionerSQLRepository
from src.core.utilities.enums import DeviceStatus, DeviceType


@pytest.fixture(scope="function")
def test_device() -> AirConditioner:
    return AirConditioner(
        id=1,
        name="Test Air Conditioner",
        status=DeviceStatus.OFF,
        degrees=23,
        type=DeviceType.AIRCONDITIONER,
    )


pg_session = create_postgres_fixture(AirConditioner, session=True, async_=True)


class TestTVSQLRepository:
    @pytest.mark.asyncio
    async def test_get_degrees(
        self, test_device: AirConditioner, pg_session: AsyncSession
    ) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo = AirConditionerSQLRepository(pg_session)
        actual_degrees = await repo.get_degrees(device_id=1)
        excepted_degrees = 23

        assert actual_degrees == excepted_degrees

    @pytest.mark.asyncio
    async def test_set_degrees(
        self, test_device: AirConditioner, pg_session: AsyncSession
    ) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo = AirConditionerSQLRepository(pg_session)
        await repo.set_degrees(device_id=1, degrees=16)

        updated_device: Type[AirConditioner] | None = await pg_session.get_one(
            AirConditioner, 1
        )
        excepted_degrees = 16

        assert updated_device is not None, "Device not found"
        assert updated_device.degrees == excepted_degrees
