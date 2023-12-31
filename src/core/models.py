from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

from src.core.utilities.constants import (
    AirConditionerSettings,
    ElectronicDeviceSettings,
    MicrowaveSettings,
    TVSettings,
)
from src.core.utilities.enums import DeviceStatus, DeviceType

Base = declarative_base()


class ElectronicDevice(Base):
    __tablename__ = "electronicdevice"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=True)
    status = Column(Enum(DeviceStatus), default=ElectronicDeviceSettings.DEFAULT_STATUS)
    type = Column(Enum(DeviceType), default=DeviceType.OTHER)
    __mapper_args__ = {
        "polymorphic_identity": DeviceType.OTHER,
        "polymorphic_on": type,
    }


class Microwave(ElectronicDevice):
    __tablename__ = "microwave"
    id = Column(Integer, ForeignKey("electronicdevice.id"), primary_key=True)
    degrees = Column(Integer, default=MicrowaveSettings.DEFAULT_DEGREES, nullable=False)
    timer = Column(Integer, default=MicrowaveSettings.DEFAULT_TIMER)
    __mapper_args__ = {"polymorphic_identity": DeviceType.MICROWAVE}


class AirConditioner(ElectronicDevice):
    __tablename__ = "airconditioner"
    id = Column(Integer, ForeignKey("electronicdevice.id"), primary_key=True)
    degrees = Column(
        Integer, default=AirConditionerSettings.DEFAULT_DEGREES, nullable=False
    )
    __mapper_args__ = {"polymorphic_identity": DeviceType.AIRCONDITIONER}


class TV(ElectronicDevice):
    __tablename__ = "tv"
    id = Column(Integer, ForeignKey("electronicdevice.id"), primary_key=True)
    channel = Column(Integer, default=TVSettings.DEFAULT_CHANNEL, nullable=False)
    __mapper_args__ = {"polymorphic_identity": DeviceType.TV}
