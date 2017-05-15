from datetime import timedelta
from typing import Dict
from .conference import Conference
from .day import Day
from .event import Event
from .room import Room


class Schedule:
    def __init__(self, conference: Conference, days: Dict[int, Day] = None, version: str = "1.0"):
        self.conference = conference

        if days:
            assert len(days) == conference.days
            self.days = days
        else:
            self.days = dict()
            for i in range(conference.days):
                index = i + 1
                self.days[index] = Day(index=index,
                                       date=conference.start + timedelta(i))

        self.version = version

    def add_room(self, name: str):
        for day in self.days.values():
            day.add_room(Room(name))

    def add_event(self, day: int, room: str, event: Event):
        self.days[day].add_event(room, event)