import datetime as dt
import logging
from fahrplan.datetime import format_datetime, parse_date, parse_datetime
from fahrplan.exception import FahrplanError
from fahrplan.xml import XmlWriter, XmlSerializable
from .event import Event
from .room import Room

log = logging.getLogger(__name__)


class Day(XmlSerializable):
    def __init__(self, index: int, date: dt.date, start: dt.datetime = None, end: dt.datetime = None):
        self.index = index
        self.date = date
        self.start = start
        self.end = end
        self.rooms = {}
        self.schedule = None

    @classmethod
    def from_dict(cls, data: dict):
        assert isinstance(data, dict), 'Data must be a dictionary.'

        obj = Day(
            index=data['index'],
            date=parse_date(data['date']),
            start=parse_datetime(data['start']),
            end=parse_datetime(data['end'])
        )
        return obj

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
        if not any(room.events for room in self.rooms.values()):
            log.warning(f"Day {self.index} has no events, skipping")
            return
        with xml.context("day", index=self.index, date=self.date,
                         start=format_datetime(self.get_start()),
                         end=format_datetime(self.get_end())):
            for room in self.rooms.values():
                xml.append_object(room, extended)
