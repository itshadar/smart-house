import pytest
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import ElectronicDevice, TV, Microwave, AirConditioner, Base
from app.core.repositories.sql_repository import SQLRepository
from pytest_mock_resources import create_postgres_fixture
from app.core.utilities import ElectronicDeviceSettings, DeviceType, MicrowaveSettings, TVSettings, \
    AirConditionerSettings


@pytest.fixture(scope='function')
def test_device() -> ElectronicDevice:
    return ElectronicDevice(id=1, name="Test Device")


@pytest.mark.asyncio
async def add_and_commit_records(pg_session, *records: Base):
    for record in records:
        pg_session.add(record)
    await pg_session.commit()


pg_session: AsyncSession = create_postgres_fixture(Base, session=True, async_=True)


@pytest.fixture(scope='function')
def sql_electronic_device_repository(pg_session: AsyncSession) -> SQLRepository:
    return SQLRepository(pg_session, ElectronicDevice)


class TestSQLRepository:

    @pytest.mark.asyncio
    async def test_create_electronic_device(self, pg_session: AsyncSession):
        data = {"name": "Test Device", "location": "Test Room"}
        repo = SQLRepository(pg_session, ElectronicDevice)
        device = await repo.create(**data)
        assert device.name == "Test Device"
        assert device.location == "Test Room"
        assert device.type == DeviceType.OTHER
        assert device.status == ElectronicDeviceSettings.DEFAULT_STATUS
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_create_microwave(self, pg_session: AsyncSession):
        data = {"name": "Test Microwave", "location": "Test Kitchen", "type": DeviceType.MICROWAVE}
        repo = SQLRepository(pg_session, Microwave)
        device = await repo.create(**data)
        assert device.name == "Test Microwave"
        assert device.location == "Test Kitchen"
        assert device.type == DeviceType.MICROWAVE
        assert device.degrees == MicrowaveSettings.DEFAULT_DEGREES
        assert device.timer == MicrowaveSettings.DEFAULT_TIMER
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_create_tv(self, pg_session: AsyncSession):
        data = {"name": "Test TV", "location": "Test TV location", "type": DeviceType.TV}
        repo = SQLRepository(pg_session, TV)
        device = await repo.create(**data)
        assert device.name == "Test TV"
        assert device.location == "Test TV location"
        assert device.type == DeviceType.TV
        assert device.channel == TVSettings.DEFAULT_CHANNEL
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_create_air_conditioner(self, pg_session: AsyncSession):
        data = {"name": "Test AC", "location": "Test AC location", "type": DeviceType.AIRCONDITIONER}
        repo = SQLRepository(pg_session, AirConditioner)
        device = await repo.create(**data)
        assert device.name == "Test AC"
        assert device.location == "Test AC location"
        assert device.type == DeviceType.AIRCONDITIONER
        assert device.degrees == AirConditionerSettings.DEFAULT_DEGREES
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_session: AsyncSession, test_device: ElectronicDevice,
                             sql_electronic_device_repository: SQLRepository):
        await add_and_commit_records(pg_session, test_device)

        actual_device = await sql_electronic_device_repository.get_by_id(id=1)

        assert actual_device == test_device

    @pytest.mark.asyncio
    async def test_list_all_electronic_devices(self, pg_session: AsyncSession,
                                               sql_electronic_device_repository: SQLRepository):
        await add_and_commit_records(pg_session,
                                     ElectronicDevice(id=1, name="Test Device"),
                                     Microwave(id=2, name="Test Microwave", type=DeviceType.MICROWAVE),
                                     Microwave(id=3, name="Test Microwave2", type=DeviceType.MICROWAVE),
                                     TV(id=4, name="Test TV", type=DeviceType.TV),
                                     AirConditioner(id=5, name="Test AC", type=DeviceType.AIRCONDITIONER))

        all_electronic_devices = await sql_electronic_device_repository.list_all()

        all_electronic_devices_ids = [device.id for device in all_electronic_devices]

        assert len(all_electronic_devices) == 5
        assert all_electronic_devices_ids == [1, 2, 3, 4, 5]

    @pytest.mark.asyncio
    async def test_list_all_microwaves(self, pg_session: AsyncSession):
        pg_session.add_all(instances=[ElectronicDevice(id=1, name="Test Device"),
                                      Microwave(id=2, name="Test Microwave", type=DeviceType.MICROWAVE),
                                      Microwave(id=3, name="Test Microwave2", type=DeviceType.MICROWAVE),
                                      TV(id=4, name="Test TV", type=DeviceType.TV),
                                      AirConditioner(id=5, name="Test AC", type=DeviceType.AIRCONDITIONER)])

        await pg_session.commit()

        microwave_repo = SQLRepository(pg_session, Microwave)

        all_microwaves = await microwave_repo.list_all()
        all_microwaves_ids = [device.id for device in all_microwaves]

        assert len(all_microwaves) == 2
        assert all_microwaves_ids == [2, 3]

    @pytest.mark.asyncio
    async def test_add(self, test_device: ElectronicDevice, pg_session: AsyncSession,
                       sql_electronic_device_repository: SQLRepository):
        await sql_electronic_device_repository.add(record=test_device)
        result = await pg_session.execute(select(ElectronicDevice).filter_by(id=1))
        actual_device = result.scalar_one_or_none()

        assert actual_device == test_device

    @pytest.mark.asyncio
    async def test_update(self, test_device: ElectronicDevice, pg_session: AsyncSession,
                          sql_electronic_device_repository: SQLRepository):
        pg_session.add(test_device)
        await pg_session.commit()

        test_device.location = "My New Location"
        await sql_electronic_device_repository.update(record=test_device)

        result = await pg_session.execute(select(ElectronicDevice).filter_by(id=1))
        updated_device = result.scalar()
        assert updated_device == test_device
        assert updated_device.location == "My New Location"

    @pytest.mark.asyncio
    async def test_delete(self, test_device: ElectronicDevice, pg_session: AsyncSession,
                          sql_electronic_device_repository: SQLRepository):
        pg_session.add(test_device)
        await pg_session.commit()

        await sql_electronic_device_repository.delete(id=1)

        result = await pg_session.execute(select(ElectronicDevice).filter_by(id=1))
        actual_device = result.one_or_none()

        assert actual_device is None
