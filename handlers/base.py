from abc import ABCMeta, abstractmethod
from configparser import ConfigParser

from fahrplan.model.schedule import Schedule


class HandlerBase(metaclass=ABCMeta):
    def __init__(self, name: str, config: ConfigParser, global_config: ConfigParser):
        self.name = name
        self.config = config
        self.global_config = global_config


class ImportHandler(HandlerBase, metaclass=ABCMeta):
    @abstractmethod
    def run(self) -> Schedule:
        pass


class ExportHandler(HandlerBase, metaclass=ABCMeta):
    @abstractmethod
    def run(self, schedule: Schedule) -> bool:
        pass
