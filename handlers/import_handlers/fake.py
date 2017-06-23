import logging

from fahrplan.datetime import parse_date, parse_datetime, parse_duration, parse_time
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from fahrplan.slug import StandardSlugGenerator
from ..base import ImportHandler
from hacks import noexcept


class FakeImportHandler(ImportHandler):
    @noexcept(logging.getLogger(__name__))
    def run(self):
        conference = Conference(
            title="DENOG8",
            acronym="denog16",
            day_count=2,
            start=parse_date("2016-11-23"),
            end=parse_date("2016-11-24"),
            time_slot_duration=parse_duration("00:10")
        )
        slug = StandardSlugGenerator(conference)
        schedule = Schedule(conference=conference)
        schedule.add_room("darmstadtium")
        schedule.add_event(1, "darmstadtium", Event(
            uid=4001, date=parse_datetime("2016-11-23T13:00:00"),
            start=parse_time("13:00"), duration=parse_duration("00:15"),
            slug=slug, title="Opening", language="en", persons={1: "DENOG ORGA"}
        ))
        schedule.add_event(2, "darmstadtium", Event(
            uid=4002, date=parse_datetime("2016-11-24T19:00:00"),
            start=parse_time("19:00"), duration=parse_duration("00:15"),
            slug=slug, title="Closing", language="en", persons={1: "DENOG ORGA"}
        ))
        return schedule
