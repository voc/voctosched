import datetime as dt

from fahrplan.datetime import format_datetime
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

    def add_room(self, room: Room):
        self.rooms[room.name] = room

    def add_event(self, room: str, event: Event):
        self.rooms[room].add_event(event)

    def get_start(self):
        if self.start is not None:
            return self.start

        return min(room.get_start() for room in self.rooms.values())

    def get_end(self):
        if self.end is not None:
            return self.end

        return max(room.get_end() for room in self.rooms.values())

    def append_xml(self, xml: XmlWriter):
        with xml.context("day", index=self.index, date=self.date,
                         start=format_datetime(self.get_start()),
                         end=format_datetime(self.get_end())):
            for room in self.rooms.values():
                xml.append_object(room)
