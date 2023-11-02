import json
import os
from anyio import run
from app.core.utilities import DeviceType
from app.core.db_operations import get_async_uow

repository_class = {DeviceType.TV: "tvs",
                    DeviceType.MICROWAVE: "microwaves",
                    DeviceType.AIRCONDITIONER: "air_conditioners"}


def read_seed_file() -> list[dict]:
    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "../seed_data/devices.json")
    with open(json_file_path, "r") as json_file:
        data_to_seed = json.load(json_file)
    return data_to_seed

def normalize_data(data_list: list[dict]):

    for data in data_list:
        data["type"] = DeviceType(data["type"])
        yield data


async def seed_data():

    data_to_seed = read_seed_file()

    async with get_async_uow() as uow:
        exist_devices = await uow.electronic_devices.list_all()
        if not exist_devices:
            for data in normalize_data(data_to_seed):
                repo = getattr(uow, repository_class.get(data["type"], "electronic_devices"))
                await repo.create(**data)


if __name__ == "__main__":
    run(seed_data)

