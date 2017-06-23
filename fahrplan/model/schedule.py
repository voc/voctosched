from datetime import date as _date, timedelta
from typing import Dict, List

from fahrplan.exception import FahrplanError
from fahrplan.xml import XmlWriter, XmlSerializable
from .conference import Conference
from .day import Day
from .event import Event
from .room import Room


class Schedule(XmlSerializable):
    def __init__(self, conference: Conference, days: Dict[int, Day] = None, version: str = "1.0"):
        self.conference = conference
        self.conference.schedule = self

        if days:
            assert len(days) == conference.day_count
            self.days = days
        else:
            # TODO (MO) document automatic day generation
            if conference.day_count and not conference.start:
                raise FahrplanError("conference.start is not set, "
                                    "cannot automatically create days.")
            self.days = {}
            for i in range(conference.day_count):
                index = i + 1
                date: _date = conference.start + timedelta(i)
                self.days[index] = Day(index=index, date=date)

        self.version = version

    def add_day(self, day: Day):
        """
        Add a day to the schedule. Beware this day will not have rooms added before.
        :return: None
        """
        self.days[day.index] = day
        self.conference.day_count += 1

    def add_room(self, name: str, day_filter: List[int] = None):
        """
        Adds a room to the days given in day_filter, or all days.
        :param name: Name of the room to be added.
        :param day_filter: List of day indices to create the room for. If empty, use all days.
        :return: None
        """
        for day in self.days.values():
            if not day_filter or day.index in day_filter:
                day.add_room(Room(name))

    def add_event(self, day: int, room: str, event: Event):
        self.days[day].add_event(room, event)

    def merge(self, other):
        # TODO (zuntrax) implement
        return self

    def append_xml(self, xml: XmlWriter, extended: bool):
        with xml.context("schedule"):
            xml.tag("version", self.version)
            xml.append_object(self.conference, extended)
            for day in self.days.values():
                xml.append_object(day, extended)
