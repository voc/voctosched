from datetime import date
from datetime import timedelta
from ..xml import XmlSerializer


class Conference:
    def __init__(self, title: str, acronym: str, days: int, start: date, end: date, timeslot_duration: timedelta):
        self.title = title
        self.acronym = acronym
        self.days = days
        self.start = start
        self.end = end
        self.timeslot_duration = timeslot_duration

    def to_xml(self, serializer=None):
        xml = serializer or XmlSerializer()
        xml.enter("conference")
        xml.tag("title", self.title)
        xml.tag("acronym", self.acronym)
        xml.tag("days", self.days)
        xml.tag("start", self.start)
        xml.tag("end", self.end)
        xml.tag("timeslot_duration", f"{str(self.timeslot_duration)[:-3]}")
        xml.exit("conference")

        if not serializer:
            return xml.buffer
