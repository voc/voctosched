from configparser import ConfigParser
from datetime import datetime, timedelta, time
from xml.sax.handler import ContentHandler

from fahrplan.datetime import parse_duration
from fahrplan.model import Conference, Day, Event, Schedule
from fahrplan.slug import StandardSlugGenerator


class ChaosradioContentHandler(ContentHandler):
    def __init__(self, config: ConfigParser):
        super().__init__()

        self.path = []
        self.room_name = config["room"]["name"]
        title = config["conference"]["title"]
        acronym = config["conference"]["acronym"]
        duration = parse_duration(config["conference"]["timeslot"])
        conference = Conference(title, acronym, time_slot_duration=duration)
        self.schedule = Schedule(conference)
        self.slug = StandardSlugGenerator(conference)

        self.next_person_id = 1
        self.known_persons = {}

        self.current_link = None

        self.event_id = None
        self.event_title = ""
        self.event_subtitle = ""
        self.event_date = None
        self.event_start = None
        self.event_duration = None
        self.event_links = {}
        self.event_download_url = ""
        self.event_persons = {}
        self.event_description = []

    def get_schedule(self):
        return self.schedule

    def startDocument(self):
        self.current_link = None

        self.event_id = None
        self.event_title = ""
        self.event_subtitle = ""
        self.event_date = None
        self.event_start = None
        self.event_duration = None
        self.event_links = {}
        self.event_download_url = ""
        self.event_persons = {}
        self.event_description = []

    def endDocument(self):
        assert self.event_id
        assert self.event_title
        assert self.event_date
        assert self.event_start
        assert self.event_duration
        assert self.event_persons

        self.schedule.add_day(Day(
            index=self.event_id,
            date=self.event_date.date()
        ))
        self.schedule.add_room(self.room_name, [self.event_id])
        description = "\n".join(self.event_description)
        # print(repr(self.event_description))
        self.schedule.add_event(day=self.event_id, room=self.room_name, event=Event(
            uid=self.event_id, date=self.event_date, start=self.event_start,
            duration=self.event_duration, title=self.event_title, language="de",
            slug=self.slug, persons=self.event_persons, recording_license="",
            subtitle=self.event_subtitle, description=description,
            download_url=self.event_download_url, links=self.event_links
        ))

    def startElement(self, name, attrs):
        self.path.append(name)
        self.dispatch_attrs(attrs)

    def endElement(self, name):
        assert self.path.pop() == name
        if self.path[:2] == ["episode", "description"]:
            if name == "p":
                self.event_description[-1] = self.event_description[-1].strip()

    def characters(self, content):
        if not content.strip():
            return
        self.dispatch_content(content)

    def dispatch_attrs(self, attrs):
        if self.path == ["episode"]:
            self.event_id = attrs["episode-no"]

        elif self.path == ["episode", "date"]:
            if attrs["type"] == "broadcast":
                self.event_date = datetime(
                    year=int(attrs["year"], 10),
                    month=int(attrs["month"], 10),
                    day=int(attrs["day"], 10),
                    hour=int(attrs["hour"], 10),
                    minute=int(attrs["minute"], 10)
                )
                self.event_start = time(
                    hour=int(attrs["hour"], 10),
                    minute=int(attrs["minute"], 10)
                )
                self.event_duration = timedelta(
                    hours=int(attrs["hours"], 10),
                    minutes=int(attrs["minutes"], 10)
                )

        elif self.path == ["episode", "link"]:
            name = attrs["rel"].capitalize().replace("-", " ")
            self.event_links[attrs["href"]] = name

        elif self.path == ["episode", "media", "media-item"]:
            # TODO (MO) which one to use?
            self.event_download_url = ""

        elif self.path[:2] == ["episode", "description"]:
            if self.path[-1] == "a":
                self.current_link = attrs["href"]
                self.event_links[self.current_link] = ""
            elif self.path[-1] == "p":
                self.event_description.append("")

    def dispatch_content(self, content):
        if self.path == ["episode", "title"]:
            self.event_title = content

        elif self.path == ["episode", "subtitle"]:
            self.event_subtitle = content

        elif self.path == ["episode", "participants", "person"]:
            if content in self.known_persons:
                person_id = self.known_persons[content]
            else:
                person_id = self.next_person_id
                self.known_persons[content] = person_id
                self.next_person_id += 1
            self.event_persons[person_id] = content

        elif self.path[:2] == ["episode", "description"]:
            if "a" in self.path:
                self.event_links[self.current_link] += content
            self.event_description[-1] += content

