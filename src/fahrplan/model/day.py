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

import datetime as dt

from fahrplan.datetime import format_datetime
from fahrplan.exception import FahrplanError
from fahrplan.xml import XmlWriter, XmlSerializable
from .event import Event
from .room import Room


class Day(XmlSerializable):
    def __init__(self, index: int, date: dt.date, start: dt.datetime = None, end: dt.datetime = None):
        self.index = index
        self.date = date
        self.start = start
        self.end = end
        self.rooms = {}
        self.schedule = None

    def add_room(self, room: Room):
        if room.name not in self.rooms:
            self.rooms[room.name] = room
            room.day = self
        # TODO (zuntrax) logging

    def add_event(self, room: str, event: Event):
        self.rooms[room].add_event(event)

    def get_start(self):
        """
        The start timestamp of the day. Returns start if explicitly set.
        Tries to infer the timestamp from assigned events, otherwise. 
        :return: start: datetime
        """
        if self.start is not None:
            return self.start

        try:
            room_starts = [room.get_start() for room in self.rooms.values()]
            return min(start for start in room_starts if start is not None)
        except ValueError:
            raise FahrplanError(f"Day {self.index} has no events, cannot infer timestamps")

    def get_end(self):
        """
        The end timestamp of the day. Returns end if explicitly set.
        Tries to infer the timestamp from assigned events, otherwise. 
        :return: end: datetime
        """
        if self.end is not None:
            return self.end

        try:
            room_ends = [room.get_end() for room in self.rooms.values()]
            return max(end for end in room_ends if end is not None)
        except ValueError:
            raise FahrplanError(f"Day {self.index} has no events, cannot infer timestamps")

    def merge(self, other: 'Day'):
        for name, room in other.rooms.items():
            if name in self.rooms:
                self.rooms[name].merge(room)
            else:
                self.rooms[name] = room
                room.day = self

    def append_xml(self, xml: XmlWriter, extended: bool):
        with xml.context("day", index=self.index, date=self.date,
                         start=format_datetime(self.get_start()),
                         end=format_datetime(self.get_end())):
            for room in self.rooms.values():
                xml.append_object(room, extended)
