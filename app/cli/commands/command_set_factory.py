from constants import DeviceType
from abc import ABC, abstractmethod
from .base_command_set import BaseCommandSet
from .electronic_device_command_set import ElectronicDeviceCommandSet
from .microwave_command_set import MicrowaveCommandSet
from .tv_command_set import TVCommandSet
from .air_conditioner_command_set import AirConditionerCommandSet


class CommandSetFactory(ABC):

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> BaseCommandSet:
        ...

    @classmethod
    @abstractmethod
    def setup(cls, *args, **kwargs):
        ...


class DeviceCommandSetFactory(CommandSetFactory):

    COMMAND_SETS = {
        DeviceType.TV: TVCommandSet,
        DeviceType.MICROWAVE: MicrowaveCommandSet,
        DeviceType.AIRCONDITIONER: AirConditionerCommandSet
    }

    @classmethod
    def create(cls, device_type, device_id, app, controller) -> ElectronicDeviceCommandSet:
        command_set_class = cls.COMMAND_SETS.get(device_type, ElectronicDeviceCommandSet)
        return command_set_class(app, controller, device_id)

    @classmethod
    def setup(cls, device_type: DeviceType, device_id, app, controller):
        device_command_set = cls.create(device_type, device_id, app, controller)
        device_command_set.register_commands()






