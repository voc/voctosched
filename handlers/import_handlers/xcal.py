from datetime import timezone, datetime, timedelta
from xml.etree import ElementTree
import logging

from binascii import crc32

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_time, parse_datetime, parse_duration
from fahrplan.model.conference import Conference
from fahrplan.model.day import Day
from fahrplan.model.event import Event
from fahrplan.model.room import Room
from fahrplan.model.schedule import Schedule
from hacks import noexcept
from util import read_input

log = logging.getLogger(__name__)


def parse_dt(inp: str) -> datetime:
    return datetime.strptime(inp, "%Y%m%dT%H%M%S")


class XcalImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        # import xcal file to dict tree
        tree = ElementTree.fromstring(read_input(self.config['path']))

        # handy references to subtrees
        vcal = tree.find('vcalendar')

        # create the conference object
        conference = Conference(
            title=self.global_config['conference']['title'],
            acronym=self.global_config['conference']['acronym'],
            day_count=int(self.global_config['conference']['day_count']),  # do not automatically generate days
            start=parse_date(self.global_config['conference']['start']),
            end=parse_date(self.global_config['conference']['end']),
            time_slot_duration=parse_duration(self.global_config['conference']['time_slot_duration'])
        )
        schedule = Schedule(conference=conference, version=vcal.find('version').text)

        days = dict()
        rooms = dict()

        for event in vcal.findall('vevent'):
            start = parse_dt(event.find('dtstart').text)
            end = parse_dt(event.find('dtend').text)
            duration = timedelta(hours=float(event.find('duration').text))
            date = start.date().isoformat()
            day = days.get(date)
            if not day:
                day = Day(
                    index=len(days),
                    date=start.date(),
                    start=start.replace(hour=0, minute=0, second=0),
                    end=start.replace(hour=23, minute=59, second=59),
                )
                schedule.add_day(day)
                days[date] = day
            
            location = event.find('location').text
            room = rooms.get(location)
            if not room:
                room = Room(location)
                rooms[location] = room
            day.add_room(Room(location))

            persons_holding_this_talk = dict()
            for attendee in event.findall('attendee'):
                name = attendee.text
                # generate some hopefully unique ids
                uid = (crc32(name.encode()) & 0xffffffff)
                persons_holding_this_talk[uid] = name
            
            links_for_this_talk = dict()
            for link in event.findall('url'):
                url = link.text
                # generate some hopefully unique ids
                links_for_this_talk[url] = url

            uid = event.find('uid').text
            day.add_event(location, Event(
                uid=uid,
                date=start.replace(tzinfo=timezone.utc),
                start=start.time(),
                duration=duration,
                slug=uid,
                title=event.find('summary').text,
                description=event.find('description').text,
                # abstract=
                language=event.find('{http://pentabarf.org}language-code').text,
                persons=persons_holding_this_talk,
                #download_url=talk.get('download_url', ''),
                #recording_license=talk.get('recording_license', ''),
                #recording_optout=talk['do_not_record'],
                #subtitle=talk.get('subtitle', ''),
                #track=talk.get('track', ''),
                event_type=event.find('category').text,
                #logo=talk.get('logo', ''),
                links=links_for_this_talk,
                #attachments=attachments
            ))

        return schedule

