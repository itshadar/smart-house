from typing import NamedTuple

from pydantic import BaseModel, Field

from src.core.utilities.constants import (AirConditionerSettings,
                                          MicrowaveSettings, TVSettings)
from src.core.utilities.enums import DeviceStatus, DeviceType


class DeviceMetadata(NamedTuple):
    name: str
    type: DeviceType
    id: int


class ElectronicDeviceDomain(BaseModel):
    id: int
    name: str
    location: str
    status: DeviceStatus
    device_type: DeviceType

    class Config:
        from_attributes = True


class MicrowaveDomain(ElectronicDeviceDomain):
    degrees: int = Field(
        ge=MicrowaveSettings.MIN_DEGREES,
        le=MicrowaveSettings.MAX_DEGREES,
        default=MicrowaveSettings.DEFAULT_DEGREES,
    )
    timer: int = Field(
        ge=MicrowaveSettings.MIN_TIMER, default=MicrowaveSettings.DEFAULT_TIMER
    )


class AirConditionerDomain(ElectronicDeviceDomain):
    degrees: int = Field(
        ge=AirConditionerSettings.MIN_DEGREES,
        le=AirConditionerSettings.MAX_DEGREES,
        default=AirConditionerSettings.DEFAULT_DEGREES,
    )


class TVDomain(ElectronicDeviceDomain):
    channel: int = Field(ge=TVSettings.MIN_CHANNEL, default=TVSettings.DEFAULT_CHANNEL)
