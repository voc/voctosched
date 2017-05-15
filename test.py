#!/usr/bin/env python3

from datetime import date, datetime, timedelta
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule


def main():
    conference = Conference(
        title="DENOG8",
        acronym="denog16",
        days=2,
        start=date(2016, 11, 23),
        end=date(2016, 11, 24),
        timeslot_duration=timedelta(minutes=10)
    )
    schedule = Schedule(conference=conference)
    schedule.add_room("darmstadtium")
    schedule.add_event(1, "darmstadtium", Event(
        uid=4001, date=datetime.strptime("2016-11-23T13:00:00", "%Y-%m-%dT%H:%M:%S"),
        start=datetime.strptime("2016-11-23T13:00:00", "%Y-%m-%dT%H:%M:%S")
        , duration=timedelta(minutes=15), slug="denog16-4001-opening",
        title="Opening", language="en", persons={1: "DENOG ORGA"}
    ))
    schedule.add_event(2, "darmstadtium", Event(
        uid=4002, date=datetime.strptime("2016-11-24T19:00:00", "%Y-%m-%dT%H:%M:%S"),
        start=datetime.strptime("2016-11-24T19:00:00", "%Y-%m-%dT%H:%M:%S"),
        duration=timedelta(minutes=15), slug="denog16-4002-closing",
        title="Closing", language="en", persons={1: "DENOG ORGA"}
    ))
    print(schedule.to_xml())


if __name__ == "__main__":
    main()
