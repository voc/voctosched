from .event import Event
from .room import Room
from ..xml import XmlSerializer


class Day:
    def __init__(self, index, date, start=None, end=None):
        self.index = index
        self.date = date
        self.start = start
        self.end = end
        self.rooms = dict()

    def add_room(self, room: Room):
        self.rooms[room.name] = room

    def add_event(self, room: str, event: Event):
        self.rooms[room].add_event(event)

    def get_start(self):
        if self.start:
            return self.start

        return min(room.get_start() for room in self.rooms.values())

    def get_end(self):
        if self.end:
            return self.end

        return max(room.get_end() for room in self.rooms.values())

    def to_xml(self, serializer=None):
        xml = serializer or XmlSerializer()
        xml.enter("day", index=self.index, date=self.date,
                  start=f"{self.get_start():%Y-%m-%dT%H:%M:%S}",
                  end=f"{self.get_end():%Y-%m-%dT%H:%M:%S}")
        for room in self.rooms.values():
            room.to_xml(xml)
        xml.exit("day")

        if not serializer:
            return xml.buffer
