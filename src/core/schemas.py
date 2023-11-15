from typing import NamedTuple, Optional

from pydantic import BaseModel, Field

from src.core.utilities.constants import (
    AirConditionerSettings,
    MicrowaveSettings,
    TVSettings,
)
from src.core.utilities.enums import DeviceStatus, DeviceType


class DeviceMetadata(NamedTuple):
    name: str
    type: DeviceType
    id: int


class ElectronicDeviceSchema(BaseModel):
    name: str
    id: Optional[int] = None
    location: Optional[str] = None
    status: Optional[DeviceStatus] = None
    type: Optional[DeviceType] = None

    # class ConfigDict:
    #     from_attributes = True


class MicrowaveSchema(ElectronicDeviceSchema):
    degrees: Optional[int] = Field(
        ge=MicrowaveSettings.MIN_DEGREES, le=MicrowaveSettings.MAX_DEGREES, default=None
    )
    timer: Optional[int] = Field(ge=MicrowaveSettings.MIN_TIMER, default=None)


class AirConditionerSchema(ElectronicDeviceSchema):
    degrees: Optional[int] = Field(
        ge=AirConditionerSettings.MIN_DEGREES,
        le=AirConditionerSettings.MAX_DEGREES,
        default=None,
    )


class TVSchema(ElectronicDeviceSchema):
    channel: Optional[int] = Field(ge=TVSettings.MIN_CHANNEL, default=None)
