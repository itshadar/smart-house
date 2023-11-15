import json
import os
from typing import Any, Dict, Iterator

from anyio import run

from src.core.db_operations import get_async_uow
from src.core.schemas import (
    AirConditionerSchema,
    ElectronicDeviceSchema,
    MicrowaveSchema,
    TVSchema,
)
from src.core.utilities.enums import DeviceType

repository_class = {
    DeviceType.TV: "tvs",
    DeviceType.MICROWAVE: "microwaves",
    DeviceType.AIRCONDITIONER: "air_conditioners",
}

device_schema_model = {
    DeviceType.TV: TVSchema,
    DeviceType.MICROWAVE: MicrowaveSchema,
    DeviceType.AIRCONDITIONER: AirConditionerSchema,
}


def read_seed_file() -> list[Dict[str, Any]]:
    json_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../seed_data/devices.json"
    )
    with open(json_file_path, "r") as json_file:
        data_to_seed = json.load(json_file)
    return data_to_seed


def normalize_data(data_list: list[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    for data in data_list:
        data["type"] = DeviceType(data["type"])
        yield data


async def seed_data() -> None:
    data_to_seed = read_seed_file()

    async with get_async_uow() as uow:
        exist_devices = await uow.electronic_devices.list_all()
        if not exist_devices:
            for data in normalize_data(data_to_seed):
                repo = getattr(
                    uow, repository_class.get(data["type"], "electronic_devices")
                )
                schema_model = device_schema_model.get(
                    data["type"], ElectronicDeviceSchema
                )
                await repo.create(schema_model(**data))


if __name__ == "__main__":
    run(seed_data)
