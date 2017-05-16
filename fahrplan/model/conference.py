from datetime import date, timedelta

from fahrplan.datetime import format_duration
from fahrplan.xml import XmlWriter, XmlSerializable


class Conference(XmlSerializable):
    def __init__(self, title: str, acronym: str, day_count: int,
                 start: date, end: date, time_slot_duration: timedelta):
        self.title = title
        self.acronym = acronym
        self.day_count = day_count
        self.start = start
        self.end = end
        self.time_slot_duration = time_slot_duration

    def append_xml(self, xml: XmlWriter):
        with xml.context("conference"):
            xml.tag("title", self.title)
            xml.tag("acronym", self.acronym)
            xml.tag("days", self.day_count)
            xml.tag("start", self.start)
            xml.tag("end", self.end)
            xml.tag("timeslot_duration", format_duration(self.time_slot_duration))
