from pydantic import ValidationError
from app.core.schemas import DeviceMetadata, ElectronicDeviceCreate
from app.core.utilities import DeviceStatus
from app.core.db_operations import UnitOfWork, get_uow


class ElectronicDeviceController:

    def create_batch(self):
        pass

    def create(self, uow: UnitOfWork, **data):
        try:
            ElectronicDeviceCreate(**data)
            uow.electronic_devices.create(**data)
        except ValidationError as e:
            raise ValidationError from e

    def get_all_devices_metadata(self) -> list[DeviceMetadata]:

        with get_uow() as uow:
            raw_data = uow.electronic_devices.get_devices_metadata()
            return [DeviceMetadata(*data) for data in raw_data]


    def get_status(self, device_id: int) -> DeviceStatus:

        with get_uow() as uow:
            status = uow.electronic_devices.get_status(device_id)
            return status

    def set_status(self, device_id: int, status: DeviceStatus):
        with get_uow() as uow:
            uow.electronic_devices.set_status(device_id, status)
