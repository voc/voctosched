from .event import Event
from .room import Room


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
