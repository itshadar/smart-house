from fastapi import APIRouter, Body, Depends, Path

from src.api.schemas import SetDeviceStatusRequest
from src.core.db_operations.unit_of_work import AsyncUnitOfWork, get_async_uow
from src.core.schemas import DeviceMetadata
from src.core.utilities.enums import DeviceStatus

router = APIRouter()


@router.get("/devices", response_model=list[DeviceMetadata])
async def list_devices(uow: AsyncUnitOfWork = Depends(get_async_uow)) -> None:
    """
    List all devices in the system.
    """
    # Implementation to list all devices
    pass


@router.get("/devices/{device_id}/status", response_model=DeviceStatus)
async def get_device_status(
    device_id: int = Path(..., description="The unique identifier of the device"),
    uow: AsyncUnitOfWork = Depends(get_async_uow),
) -> None:
    """
    Get the status of a specific device.
    """
    # Implementation to get the status of a specific device
    pass


@router.put("/devices/{device_id}/status", response_model=DeviceStatus)
async def set_device_status(
    device_id: int = Path(..., description="The unique identifier of the device"),
    status: SetDeviceStatusRequest = Body(
        ..., description="New status to set for the device"
    ),
    uow: AsyncUnitOfWork = Depends(get_async_uow),
) -> None:
    """
    Set the status of a specific device.
    """
    # Implementation to set the status of a specific device
    pass
