from datetime import date, timedelta
from typing import Union

from fahrplan.datetime import format_duration
from fahrplan.exception import FahrplanError
from fahrplan.xml import XmlWriter, XmlSerializable


class Conference(XmlSerializable):
    # TODO (MO) what is time_slot_duration even used for?
    def __init__(self, title: str, acronym: str, day_count: int = 0,
                 start: Union[date, None] = None, end: Union[date, None] = None,
                 time_slot_duration: timedelta = None):
        self.title = title
        self.acronym = acronym
        self.day_count = day_count
        self.start = start
        self.end = end
        self.time_slot_duration = time_slot_duration
        self.schedule = None

    def get_start(self):
        if self.start:
            return self.start
        starts = []
        for day in self.schedule.days.values():
            try:
                starts.append(day.get_start())
            except FahrplanError:
                continue
        try:
            return min(starts).date()
        except ValueError:
            raise FahrplanError("No events in schedule, cannot infer dates")

    def get_end(self):
        if self.end:
            return self.end
        starts = []
        for day in self.schedule.days.values():
            try:
                # We want to use start here because last day might extend beyond midnight
                starts.append(day.get_start())
            except FahrplanError:
                continue
        try:
            return max(starts).date()
        except ValueError:
            raise FahrplanError("No events in schedule, cannot infer dates")

    def append_xml(self, xml: XmlWriter, extended: bool):
        with xml.context("conference"):
            xml.tag("title", self.title)
            xml.tag("acronym", self.acronym)
            xml.tag("days", self.day_count)
            xml.tag("start", self.get_start())
            xml.tag("end", self.get_end())
            xml.tag("timeslot_duration", format_duration(self.time_slot_duration))
