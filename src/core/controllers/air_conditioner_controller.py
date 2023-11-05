from .electronic_device_controller import ElectronicDeviceController
from app.core.schemas import AirConditionerCreate
from pydantic import ValidationError
from app.core.db_operations import get_uow


class AirConditionerController(ElectronicDeviceController):

    def create(self, *records):
        with get_uow() as uow:
            for record in records:
                try:
                    AirConditionerCreate(**record)
                    uow.air_conditioners.create(**record)

                except ValidationError as e:
                    raise ValidationError from e

    def get_degrees(self, device_id: int) -> int:
        with get_uow() as uow:
            result = uow.air_conditioners.get_degrees(device_id)
            return result

    def set_degrees(self, device_id: int, degrees: int):
        with get_uow() as uow:
            result = uow.air_conditioners.set_degrees(device_id, degrees)
