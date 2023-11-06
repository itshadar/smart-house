from abc import ABC, abstractmethod

from src.cli.commands.air_conditioner_command_set import \
    AirConditionerCommandSet
from src.cli.commands.base_command_set import BaseCommandSet
from src.cli.commands.electronic_device_command_set import \
    ElectronicDeviceCommandSet
from src.cli.commands.microwave_command_set import MicrowaveCommandSet
from src.cli.commands.tv_command_set import TVCommandSet
from src.core.utilities.enums import DeviceType


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
        DeviceType.AIRCONDITIONER: AirConditionerCommandSet,
    }

    @classmethod
    def create(cls, device_type: DeviceType, app) -> ElectronicDeviceCommandSet:
        command_set_class = cls.COMMAND_SETS.get(
            device_type, ElectronicDeviceCommandSet
        )
        return command_set_class(app)

    @classmethod
    def setup(cls, device_type: DeviceType, app):
        device_command_set = cls.create(device_type, app)
        device_command_set.register_commands()
