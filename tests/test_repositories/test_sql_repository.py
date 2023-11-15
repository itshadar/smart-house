import pytest
from typing import Type
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import (TV, AirConditioner, Base, ElectronicDevice,
                             Microwave)

from src.core.schemas import ElectronicDeviceSchema, AirConditionerSchema, MicrowaveSchema, TVSchema
from src.core.repositories.sql_repository import SQLRepository
from src.core.utilities.constants import (AirConditionerSettings,
                                          ElectronicDeviceSettings,
                                          MicrowaveSettings, TVSettings)
from src.core.utilities.enums import DeviceType


@pytest.fixture(scope='function')
def test_device() -> ElectronicDevice:
    return ElectronicDevice(id=1, name="Test Device")


pg_session: AsyncSession = create_postgres_fixture(Base, session=True, async_=True)


@pytest.fixture(scope='function')
def sql_electronic_device_repository(pg_session: AsyncSession) -> SQLRepository[ElectronicDevice, ElectronicDeviceSchema]:
    return SQLRepository(pg_session, ElectronicDevice)


class TestSQLRepository:

    @pytest.mark.asyncio
    async def test_create_electronic_device(self, pg_session: AsyncSession) -> None:
        electronic_device_schema = ElectronicDeviceSchema(name="Test Device", location="Test Room")
        repo: SQLRepository[ElectronicDevice, ElectronicDeviceSchema] = SQLRepository(pg_session, ElectronicDevice)
        device: ElectronicDevice = await repo.create(electronic_device_schema)
        assert device.name == "Test Device"
        assert device.location == "Test Room"
        assert device.type == DeviceType.OTHER
        assert device.status == ElectronicDeviceSettings.DEFAULT_STATUS
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_create_microwave(self, pg_session: AsyncSession) -> None:
        microwave_schema = MicrowaveSchema(name="Test Microwave", location="Test Kitchen", type=DeviceType.MICROWAVE)
        repo: SQLRepository[Microwave, MicrowaveSchema] = SQLRepository(pg_session, Microwave)
        device: Microwave = await repo.create(microwave_schema)
        assert device.name == "Test Microwave"
        assert device.location == "Test Kitchen"
        assert device.type == DeviceType.MICROWAVE
        assert device.degrees == MicrowaveSettings.DEFAULT_DEGREES
        assert device.timer == MicrowaveSettings.DEFAULT_TIMER
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_create_tv(self, pg_session: AsyncSession) -> None:
        tv_schema = TVSchema(name="Test TV", location="Test TV location", type=DeviceType.TV)
        repo: SQLRepository[TV, TVSchema] = SQLRepository(pg_session, TV)
        device: TV = await repo.create(tv_schema)
        assert device.name == "Test TV"
        assert device.location == "Test TV location"
        assert device.type == DeviceType.TV
        assert device.channel == TVSettings.DEFAULT_CHANNEL
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_create_air_conditioner(self, pg_session: AsyncSession) -> None:
        ac_schema = AirConditionerSchema(name="Test AC", location="Test AC location", type=DeviceType.AIRCONDITIONER)
        repo: SQLRepository[AirConditioner, AirConditionerSchema] = SQLRepository(pg_session, AirConditioner)
        device: AirConditioner = await repo.create(ac_schema)
        assert device.name == "Test AC"
        assert device.location == "Test AC location"
        assert device.type == DeviceType.AIRCONDITIONER
        assert device.degrees == AirConditionerSettings.DEFAULT_DEGREES
        assert device.id is not None

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_session: AsyncSession, test_device: ElectronicDevice,
                             sql_electronic_device_repository: SQLRepository[ElectronicDevice, ElectronicDeviceSchema]) -> None:
        pg_session.add(test_device)

        actual_device = await sql_electronic_device_repository.get_by_id(record_id=1)

        assert actual_device == test_device

    @pytest.mark.asyncio
    async def test_list_all_electronic_devices(self, pg_session: AsyncSession,
                                               sql_electronic_device_repository: SQLRepository[ElectronicDevice, ElectronicDeviceSchema]) -> None:

        pg_session.add_all(instances=[ElectronicDevice(id=1, name="Test Device"),
                                            Microwave(id=2, name="Test Microwave", type=DeviceType.MICROWAVE),
                                            Microwave(id=3, name="Test Microwave2", type=DeviceType.MICROWAVE),
                                            TV(id=4, name="Test TV", type=DeviceType.TV),
                                            AirConditioner(id=5, name="Test AC", type=DeviceType.AIRCONDITIONER)])

        all_electronic_devices: list[ElectronicDevice] = await sql_electronic_device_repository.list_all()
        all_electronic_devices_ids = [device.id for device in all_electronic_devices]

        assert len(all_electronic_devices) == 5
        assert all_electronic_devices_ids == [1, 2, 3, 4, 5]

    @pytest.mark.asyncio
    async def test_list_all_microwaves(self, pg_session: AsyncSession) -> None:
        pg_session.add_all(instances=[ElectronicDevice(id=1, name="Test Device"),
                                      Microwave(id=2, name="Test Microwave", type=DeviceType.MICROWAVE),
                                      Microwave(id=3, name="Test Microwave2", type=DeviceType.MICROWAVE),
                                      TV(id=4, name="Test TV", type=DeviceType.TV),
                                      AirConditioner(id=5, name="Test AC", type=DeviceType.AIRCONDITIONER)])

        await pg_session.commit()

        microwave_repo: SQLRepository[Microwave, MicrowaveSchema] = SQLRepository(pg_session, Microwave)

        all_microwaves: list[Microwave] = await microwave_repo.list_all()
        all_microwaves_ids = [device.id for device in all_microwaves]

        assert len(all_microwaves) == 2
        assert all_microwaves_ids == [2, 3]

    @pytest.mark.asyncio
    async def test_add(self, test_device: ElectronicDevice, pg_session: AsyncSession,
                       sql_electronic_device_repository: SQLRepository[ElectronicDevice, ElectronicDeviceSchema]) -> None:
        await sql_electronic_device_repository.add(record=test_device)
        actual_device: Type[ElectronicDevice] | None = await pg_session.get_one(ElectronicDevice, 1)

        assert actual_device is not None, "Device not found"
        assert actual_device == test_device

    @pytest.mark.asyncio
    async def test_update(self, test_device: ElectronicDevice, pg_session: AsyncSession,
                          sql_electronic_device_repository: SQLRepository[ElectronicDevice, ElectronicDeviceSchema]) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        test_device.location = "TestLocation"

        await sql_electronic_device_repository.update(record=test_device)

        updated_device: Type[ElectronicDevice] | None = await pg_session.get_one(ElectronicDevice, 1)

        assert updated_device is not None, "Device not found"
        assert updated_device == test_device
        assert updated_device.location == "TestLocation"

    @pytest.mark.asyncio
    async def test_delete(self, test_device: ElectronicDevice, pg_session: AsyncSession,
                          sql_electronic_device_repository: SQLRepository[ElectronicDevice, ElectronicDeviceSchema]) -> None:
        pg_session.add(test_device)
        await pg_session.commit()

        await sql_electronic_device_repository.delete(record_id=1)

        actual_device: Type[ElectronicDevice] | None = await pg_session.get(ElectronicDevice, 1)

        assert actual_device is None
