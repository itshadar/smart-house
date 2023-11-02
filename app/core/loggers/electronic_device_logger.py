import logging


class ElectronicDeviceCommandLogger(logging.Logger):

    def set_log(self, device_name: str, attr: str, attr_value: any):
        self.info(f"Set {device_name} {attr} to {attr_value}")

    def get_log(self, device_name: str, attr: str, attr_value: any):
        self.info(f"{device_name} {attr} is {attr_value}")
