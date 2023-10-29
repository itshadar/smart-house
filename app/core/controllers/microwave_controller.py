from .electronic_device_controller import ElectronicDeviceController
from app.core.schemas import MicrowaveCreate
from pydantic import ValidationError
from app.core.db_operations import get_uow, UnitOfWork


class MicrowaveController(ElectronicDeviceController):

    def create(self, uow, **data):

        try:
            MicrowaveCreate(**data)
            uow.microwaves.create(**data)

        except ValidationError as e:
            raise ValidationError from e

        #  except SQLAlchemyError as e:


    def get_degrees(self, device_id: int) -> int:
        with get_uow() as uow:
            return uow.microwaves.get_degrees(device_id)


    def set_degrees_and_timer(self, device_id: int, degrees: int, timer: int):
        with get_uow() as uow:
            uow.microwaves.set_degrees_and_timer(device_id, degrees, timer)

