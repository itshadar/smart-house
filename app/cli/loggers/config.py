import logging
from .handlers import get_typer_handler
from app.core.loggers import ElectronicDeviceLogger


def configure_cli_logger(name: str = 'cli') -> ElectronicDeviceLogger:
    logging.setLoggerClass(ElectronicDeviceLogger)
    logger = logging.getLogger(name)
    logger.addHandler(get_typer_handler())
    logger.setLevel(logging.DEBUG)
    return logger
