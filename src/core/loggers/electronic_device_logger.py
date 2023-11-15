import logging
from typing import Any


class ElectronicDeviceLogger(logging.Logger):
    def set_log(self, device_name: str, attr: str, attr_value: Any) -> None:
        self.info("Set %s %s to %s", device_name, attr, attr_value)  # G004

    def get_log(self, device_name: str, attr: str, attr_value: Any) -> None:
        self.info("%s %s is %s", device_name, attr, attr_value)  # G004
