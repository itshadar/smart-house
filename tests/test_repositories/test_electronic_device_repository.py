import pytest
from typing import Type
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import ElectronicDevice
from src.core.schemas import ElectronicDeviceSchema
from src.core.repositories.electronic_device_repository import (
    ElectronicDeviceSQLRepository,
)
from src.core.utilities.enums import DeviceStatus, DeviceType


@pytest.fixture(scope="function")
def test_device() -> ElectronicDevice:
    return ElectronicDevice(id=1, name="Test Device", status=DeviceStatus.OFF)


pg_session = create_postgres_fixture(ElectronicDevice, session=True, async_=True)


class TestElectronicDeviceSQLRepository:
    @pytest.mark.asyncio
    async def test_get_devices_metadata(
        self, test_device: ElectronicDevice, pg_session: AsyncSession
    ) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo: ElectronicDeviceSQLRepository[
            ElectronicDevice, ElectronicDeviceSchema
        ] = ElectronicDeviceSQLRepository(pg_session)

        devices_metadata = await repo.get_devices_metadata()
        assert len(devices_metadata) == 1
        assert devices_metadata[0].name == "Test Device"
        assert devices_metadata[0].id == 1
        assert devices_metadata[0].type == DeviceType.OTHER

    @pytest.mark.asyncio
    async def test_get_status(
        self, test_device: ElectronicDevice, pg_session: AsyncSession
    ) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo: ElectronicDeviceSQLRepository[
            ElectronicDevice, ElectronicDeviceSchema
        ] = ElectronicDeviceSQLRepository(pg_session)
        actual_status = await repo.get_status(device_id=1)
        excepted_status = DeviceStatus.OFF

        assert actual_status == excepted_status

    @pytest.mark.asyncio
    async def test_set_status(
        self, test_device: ElectronicDevice, pg_session: AsyncSession
    ) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        repo: ElectronicDeviceSQLRepository[
            ElectronicDevice, ElectronicDeviceSchema
        ] = ElectronicDeviceSQLRepository(pg_session)
        await repo.set_status(device_id=1, status=DeviceStatus.ON)

        updated_device: Type[ElectronicDevice] | None = await pg_session.get(
            ElectronicDevice, 1
        )

        excepted_status = DeviceStatus.ON

        assert updated_device is not None, "Device not found"
        assert updated_device.status == excepted_status
