from app.core.utilities import DeviceType
from .electronic_device_controller import ElectronicDeviceController
from .air_conditioner_controller import AirConditionerController
from .tv_controller import TVController
from .microwave_controller import MicrowaveController


class ControllerFactory:

    CONTROLLERS = {
        DeviceType.TV: TVController,
        DeviceType.MICROWAVE: MicrowaveController,
        DeviceType.AIRCONDITIONER: AirConditionerController
    }

    @classmethod
    def create(cls, device_type: DeviceType) -> ElectronicDeviceController:
        controller_cls = cls.CONTROLLERS.get(device_type, ElectronicDeviceController)
        return controller_cls()
