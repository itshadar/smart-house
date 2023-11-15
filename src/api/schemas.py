from pydantic import BaseModel, Field

from src.core.utilities.constants import MicrowaveSettings
from src.core.utilities.enums import DeviceStatus


class SetDeviceStatusRequest(BaseModel):
    status: DeviceStatus


class SetMicrowaveControlsRequest(BaseModel):
    degrees: int = Field(
        ge=MicrowaveSettings.MIN_DEGREES, le=MicrowaveSettings.MAX_DEGREES
    )
    timer: int = Field(ge=MicrowaveSettings.MIN_TIMER)


class SetAirConditionerDegreesRequest(BaseModel):
    degrees: int


class SetTVChannelRequest(BaseModel):
    channel: int
