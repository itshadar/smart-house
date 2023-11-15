class RecordNotFoundError(Exception):
    """Exception raised when a record is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message)


class DeviceNotFoundError(RecordNotFoundError):
    """Exception raised when a record is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message)
