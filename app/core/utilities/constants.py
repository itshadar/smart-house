from .enums import DeviceStatus, DeviceType


class ElectronicDeviceSettings:
    DEFAULT_STATUS = DeviceStatus.OFF


class MicrowaveSettings:
    MAX_DEGREES = 30
    MIN_DEGREES = 20
    DEFAULT_DEGREES = 25
    MIN_TIMER = 0
    DEFAULT_TIMER = 0


class AirConditionerSettings:
    MAX_DEGREES = 30
    MIN_DEGREES = 10
    DEFAULT_DEGREES = 25


class TVSettings:
    MIN_CHANNEL = 0
    MAX_CHANNEL = 10000
    DEFAULT_CHANNEL = 0

