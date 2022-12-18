import logging

from fahrplan.xml import XmlWriter, XmlSerializable
from .event import Event

log = logging.getLogger(__name__)


class Room(XmlSerializable):
    def __init__(self, name: str, guid: str = None):
        self.name = name
        self.guid = guid
        self.events = dict()
        self.day = None

    @classmethod
    def from_dict(cls, data: dict, pop_used_keys=False):
        """
        Loads an Room instance from the given dictionary.
        An existing event can be provided which's data is overwritten (in parts).

        :param data: a dictionary containing Room attributes' names as key (and their values)
        :param pop_used_keys: Remove 'used' keys from the provided data. This can be used to detect additional/errornous fields.

        """
        assert isinstance(data, dict), 'Data must be a dictionary.'

        obj = Room(name=data['name'])
        direct_fields = ['guid']  # 'description', 'blocked', 'capacity']
        integer_fields = ['capacity']
        for fld in direct_fields:
            if fld in data:
                value = data[fld] if not pop_used_keys else data.pop(fld)
                if fld in integer_fields:
                    value = int(value)
                setattr(obj, fld, value)
        return obj

    def add_event(self, event: Event):
        event.room = self
        self.events[event.id] = event

    def get_start(self):
        try:
            return min(event.date for event in self.events.values())
        except ValueError:
            # No events assigned
            return None

    def get_end(self):
        try:
            return max(event.date + event.duration for event in self.events.values())
        except ValueError:
            # No events assigned
            return None

    def merge(self, other: 'Room'):
        for uid, event in other.events.items():
            if self.day.schedule.has_collision(event):
                log.warning(f'event collision while adding: "{event}"')
                continue
            self.add_event(event)

    def append_xml(self, xml: XmlWriter, extended: bool):
        with xml.context("room", name=self.name):
            for event in self.events.values():
                xml.append_object(event, extended)
