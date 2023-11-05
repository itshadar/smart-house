from pydantic import Field, BaseModel
from typing import Optional, NamedTuple
from app.core.utilities import AirConditionerSettings, MicrowaveSettings, TVSettings, DeviceStatus, DeviceType


class DeviceMetadata(NamedTuple):

    name: str
    type: DeviceType
    id: int


class ElectronicDeviceCreate(BaseModel):

    name: str
    location: Optional[str]
    status: Optional[DeviceStatus]
    type: DeviceType


class AirConditionerCreate(ElectronicDeviceCreate):
    degrees: int = Field(ge=AirConditionerSettings.MIN_DEGREES, le=AirConditionerSettings.MAX_DEGREES,
                         default=AirConditionerSettings.DEFAULT_DEGREES)


class MicrowaveCreate(ElectronicDeviceCreate):
    degrees: int = Field(ge=MicrowaveSettings.MIN_DEGREES, le=MicrowaveSettings.MAX_DEGREES, default=MicrowaveSettings.DEFAULT_DEGREES)
    timer: int = Field(ge=MicrowaveSettings.MIN_TIMER, default=MicrowaveSettings.DEFAULT_TIMER)


class TVCreate(ElectronicDeviceCreate):
    channel: int = Field(ge=TVSettings.MIN_CHANNEL, default=TVSettings.DEFAULT_CHANNEL)



