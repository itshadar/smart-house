import json
import os
from constants import DeviceType
from database import get_session, UnitOfWork
from app.core.controllers import ControllerFactory

json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../seed_data/devices.json")  # TODO: USE PICKLE?
# Load data from the JSON file
with open(json_file_path, "r") as json_file:
    data_to_insert_list = json.load(json_file)


def seed_data():

    # # todo: validate json data
    with UnitOfWork(get_session) as uow:

        for data in data_to_insert_list:

            data["type"] = DeviceType(data["type"])
            controller = ControllerFactory.create(data["type"], uow)
            controller.create(**data)


if __name__ == "__main__":
    seed_data()

