from abc import ABC, abstractmethod

from typer import Typer


class BaseCommandSet(ABC):
    def __init__(self, app: Typer):
        self.app = app

    def register_commands(self):
        self.commands()

    @abstractmethod
    def commands(self):
        ...
