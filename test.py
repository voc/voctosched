#!/usr/bin/env python3

from fahrplan.model.event import Event
from datetime import datetime, timedelta


def main():
    now = datetime.now()
    duration = timedelta(hours=1, minutes=30)
    ev = Event(1337, now, now, duration, "hurrdurr", "de", "blubb-1337-hurrdurr", "CC-BY-SA 4.0", False,
               persons={4711: "SpamAndEggs"}, download_url="https://example.com")
    print(ev.to_xml())


if __name__ == "__main__":
    main()