from datetime import date, timedelta

from ..xml import XmlSerializer


# TODO (AK) create an abstract base class XMLSerializable (with ABCMeta) that has a public method to_xml,
# which receives the serializer or creates a default one. This method should then delegate to an abstract method that
# is implemented in sub-classes for serialization. With this base class a class. Change all other model classes the
# same way.
# TODO (AK) rename all timeslot occurrences to time_slot
class Conference:
    def __init__(self, title: str, acronym: str, days: int, start: date, end: date, timeslot_duration: timedelta):
        self.title = title
        self.acronym = acronym
        # TODO (AK) rename days to number_of_days or similar
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
        # TODO (AK) extract method for str(self.timeslot_duration)[:-3] that has a proper name which explains the
        # meaning of this expression
        xml.tag("timeslot_duration", f"{str(self.timeslot_duration)[:-3]}")
        xml.exit("conference")

        # TODO (AK) What is returned if serializer is not none? I find it quite confusing that this method is
        # sometimes returning a value and sometimes just contributing to a given serializer.
        if not serializer:
            return xml.buffer
