#!/usr/bin/env python3

from fahrplan.datetime import parse_date, parse_datetime, parse_duration, parse_time
from fahrplan.model import Conference, Event, Schedule


# TODO (AK) for test cases, i would advise proper unit tests, with the nosetests runner, for details contact me directly

def main():
    conference = Conference(
        title="DENOG8",
        acronym="denog16",
        day_count=2,
        start=parse_date("2016-11-23"),
        end=parse_date("2016-11-24"),
        time_slot_duration=parse_duration("00:10")
    )
    schedule = Schedule(conference=conference)
    schedule.add_room("darmstadtium")
    schedule.add_event(1, "darmstadtium", Event(
        uid=4001, date=parse_datetime("2016-11-23T13:00:00"),
        start=parse_time("13:00"), duration=parse_duration("00:15"),
        slug="denog16-4001-opening", title="Opening", language="en",
        persons={1: "DENOG ORGA"}
    ))
    schedule.add_event(2, "darmstadtium", Event(
        uid=4002, date=parse_datetime("2016-11-24T19:00:00"),
        start=parse_time("19:00"), duration=parse_duration("00:15"),
        slug="denog16-4002-closing", title="Closing", language="en",
        persons={1: "DENOG ORGA"}
    ))
    print(schedule.to_xml())


if __name__ == "__main__":
    main()
