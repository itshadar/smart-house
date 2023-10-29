from models import ElectronicDevice
from schemas import DeviceMetadata
from .sql_repository import SQLRepository
from constants import DeviceStatus

class ElectronicDeviceRepository(SQLRepository):

    _model = ElectronicDevice

    def __init__(self, session):
        super().__init__(session, self._model)

    def get_devices_metadata(self, **filters) -> list[tuple]:
        statement = self._build_statement(*DeviceMetadata._fields, **filters)
        return self._session.execute(statement).all()

    def get_status(self, device_id: int):
        return self._session.query(self._model.status).filter_by(id=device_id).scalar()

    def set_status(self, device_id: int, status: DeviceStatus):
        device = self.get_by_id(device_id)
        device.status = status
        self.update(device)

