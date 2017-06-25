# This file is part of voctosched, a frab schedule converter.
# Copyright (C) 2017-2017 Markus Otto <otto@fs.tum.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
