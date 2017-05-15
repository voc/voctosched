from .event import Event
from .room import Room
from ..xml import XmlSerializer


# TODO (AK) see comments in conference.py about xml serialization
class Day:
    # TODO (AK) add type annotations
    def __init__(self, index, date, start=None, end=None):
        self.index = index
        self.date = date
        self.start = start
        self.end = end
        # TODO (AK) use literal {} for dict construction
        self.rooms = dict()

    def add_room(self, room: Room):
        self.rooms[room.name] = room

    def add_event(self, room: str, event: Event):
        self.rooms[room].add_event(event)

    def get_start(self):
        # TODO (AK) what type has start? If start is an integer value, it may be zero and thus self.start evaluates
        # to false, although you want to return self.start directly in this case. Therefore check for self.start is None
        if self.start:
            return self.start

        return min(room.get_start() for room in self.rooms.values())

    def get_end(self):
        # TODO (AK) same as above in get_start
        if self.end:
            return self.end

        return max(room.get_end() for room in self.rooms.values())

    def to_xml(self, serializer=None):
        xml = serializer or XmlSerializer()
        # TODO (AK) extract date format string into a constant with proper name. Further extract a method for start
        # and end formatting to deduplicate the formatting
        xml.enter("day", index=self.index, date=self.date,
                  start=f"{self.get_start():%Y-%m-%dT%H:%M:%S}",
                  end=f"{self.get_end():%Y-%m-%dT%H:%M:%S}")
        for room in self.rooms.values():
            room.to_xml(xml)
        xml.exit("day")

        if not serializer:
            return xml.buffer
