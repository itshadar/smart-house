from models import TV
from .electronic_device_repository import ElectronicDeviceRepository


class TVRepository(ElectronicDeviceRepository):

    _model = TV

    def get_channel(self, id: int):
        return self._session.query(self._model.channel).filter_by(id=id).scalar()

    def set_channel(self, id: int, channel: int):
        tv = self.get_by_id(id)
        tv.channel = channel
        self.update(tv)
