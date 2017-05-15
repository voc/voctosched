from .event import Event
from ..xml import XmlSerializer


# TODO (AK) see comments in conference.py about xml serialization
class Room:
    def __init__(self, name: str):
        self.name = name
        self.events = dict()

    def add_event(self, event: Event):
        event.room = self.name
        self.events[event.id] = event

    def get_start(self):
        return min(event.start for event in self.events.values())

    def get_end(self):
        return max(event.start + event.duration for event in self.events.values())

    def to_xml(self, serializer=None):
        xml = serializer or XmlSerializer()
        xml.enter("room", name=self.name)
        for event in self.events.values():
            event.to_xml(xml)
        xml.exit("room")

        if not serializer:
            return xml.buffer
