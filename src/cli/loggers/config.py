import logging
from typing import cast
from .handlers import get_typer_handler
from src.core.loggers.electronic_device_logger import ElectronicDeviceLogger


def configure_cli_logger(name: str = 'cli') -> ElectronicDeviceLogger:
    logging.setLoggerClass(ElectronicDeviceLogger)
    logger = logging.getLogger(name)
    logger.addHandler(get_typer_handler())
    logger.setLevel(logging.DEBUG)
    return cast(ElectronicDeviceLogger, logger)
