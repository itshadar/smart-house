from .electronic_device_controller import ElectronicDeviceController
from app.core.schemas import TVCreate
from pydantic import ValidationError
from app.core.db_operations import get_uow


class TVController(ElectronicDeviceController):

    def create(self, uow, **data):

        try:
            TVCreate(**data)
            uow.tvs.create(**data)

        except ValidationError as e:
            raise ValidationError from e

    def switch_channel(self, device_id: int, channel: int):
        with get_uow() as uow:
            uow.tvs.set_channel(device_id, channel)

    def get_channel(self, device_id: int) -> int:
        with get_uow() as uow:
            return uow.tvs.get_channel(device_id)
