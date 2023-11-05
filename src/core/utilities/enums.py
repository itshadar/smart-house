from enum import Enum


class DeviceStatus(Enum):
    ON = "ON"
    OFF = "OFF"


class DeviceType(Enum):
    TV = "tv"
    MICROWAVE = "microwave"
    AIRCONDITIONER = "airconditioner"
    OTHER = "other"

