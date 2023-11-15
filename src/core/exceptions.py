class RecordNotFoundException(Exception):
    """Exception raised when a record is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message)


class DeviceNotFoundException(RecordNotFoundException):
    """Exception raised when a record is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message)
