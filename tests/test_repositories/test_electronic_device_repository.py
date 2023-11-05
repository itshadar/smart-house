import pytest
from sqlalchemy.sql import select
from app.core.models import ElectronicDevice
from app.core.schemas import DeviceMetadata
from app.core.utilities import DeviceStatus, DeviceType
from app.core.repositories import ElectronicDeviceSQLRepository
from pytest_mock_resources import create_postgres_fixture


@pytest.fixture(scope='function')
def test_device():
    return ElectronicDevice(id=1, name="Test Device", status=DeviceStatus.OFF)


pg_session = create_postgres_fixture(ElectronicDevice, session=True, async_=True)


class TestElectronicDeviceSQLRepository:

    @pytest.mark.asyncio
    async def test_get_devices_metadata(self, test_device, pg_session):
        pg_session.add(test_device)
        await pg_session.commit()

        repo = ElectronicDeviceSQLRepository(pg_session)
        # TODO: DEAL WITH THIS FUNCTION TO RETURN METADATA
        devices_metadata = await repo.get_devices_metadata()
        assert len(devices_metadata) == 1
        assert devices_metadata[0].name == "Test Device"
        assert devices_metadata[0].id == 1
        assert devices_metadata[0].type == DeviceType.OTHER

    @pytest.mark.asyncio
    async def test_get_status(self, test_device, pg_session):
        pg_session.add(test_device)
        await pg_session.commit()

        repo = ElectronicDeviceSQLRepository(pg_session)
        actual_status = await repo.get_status(device_id=1)
        excepted_status = DeviceStatus.OFF

        assert actual_status == excepted_status

    @pytest.mark.asyncio
    async def test_set_status(self, test_device, pg_session):
        pg_session.add(test_device)
        await pg_session.commit()

        repo = ElectronicDeviceSQLRepository(pg_session)
        await repo.set_status(device_id=1, status=DeviceStatus.ON)

        result = await pg_session.execute(select(ElectronicDevice).filter_by(id=1))
        updated_device = result.scalar()
        excepted_status = DeviceStatus.ON

        assert updated_device.status == excepted_status
