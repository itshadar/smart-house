from models import AirConditioner
from .electronic_device_repository import ElectronicDeviceRepository


class AirConditionerRepository(ElectronicDeviceRepository):

    _model = AirConditioner

    def get_degrees(self, id: int) -> int:
        return self._session.query(self._model.degrees).filter_by(id=id).scalar()

    def set_degrees(self, id: int, degrees: int):
        ac = self.get_by_id(id)
        ac.degrees = degrees
        self.update(ac)

