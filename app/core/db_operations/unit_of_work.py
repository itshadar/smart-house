from app.core.repositories import ElectronicDeviceRepository, MicrowaveRepository, TVRepository, AirConditionerRepository
from abc import ABC, abstractmethod
from typing import Callable
from sqlalchemy.orm import Session
from .session import get_session

class UnitOfWorkBase(ABC):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            self.rollback()
            raise exc_type
        else:
            self.commit()
        self.close()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self._session = None

    def __enter__(self):
        self._session = self._session_factory()
        return super().__enter__()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    def close(self):
        self._session.close()
        self._session = None

    @property
    def electronic_devices(self):
        return ElectronicDeviceRepository(self._session)

    @property
    def microwaves(self):
        return MicrowaveRepository(self._session)

    @property
    def tvs(self):
        return TVRepository(self._session)

    @property
    def air_conditioners(self):
        return AirConditionerRepository(self._session)


def get_uow():
     return UnitOfWork(get_session)
