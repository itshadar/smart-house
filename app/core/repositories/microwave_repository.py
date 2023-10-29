from models import Microwave
from .electronic_device_repository import ElectronicDeviceRepository


class MicrowaveRepository(ElectronicDeviceRepository):

    _model = Microwave

    def get_degrees(self, id: int) -> int:
        return self._session.query(self._model.degrees).filter_by(id=id).scalar()

    def set_degrees_and_timer(self, id: int, degrees: int, timer: int):
        microwave = self.get_by_id(id)
        microwave.degrees = degrees
        microwave.timer = timer
        self.update(microwave)



