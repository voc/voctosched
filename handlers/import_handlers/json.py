import json
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
from util import read_file


log = logging.getLogger(__name__)


class JSONImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        # import json file to dict tree
        tree = json.loads(read_file(self.config['path']))

        # handy references to subtrees
        conf_tree = tree['schedule']['conference']

        # create the conference object
        conference = Conference(
            title=conf_tree['title'],
            acronym=conf_tree['acronym'],
            day_count=0,  # do not automatically generate days
            start=parse_date(conf_tree['start']),
            end=parse_date(conf_tree['end']),
            time_slot_duration=parse_duration(conf_tree['timeslot_duration'])
        )
        schedule = Schedule(conference=conference, version=tree['schedule']['version'])

        for day_tree in conf_tree['days']:
            day = Day(
                index=day_tree['index'],
                date=parse_date(day_tree['date']),
                start=parse_datetime(day_tree['start']),
                end=parse_datetime(day_tree['end'])
            )
            schedule.add_day(day)

            for room_name, room_talks in day_tree['rooms'].items():
                day.add_room(Room(room_name))

                for talk in room_talks:
                    persons = {}
                    for person_info in talk['persons']:
                        name = person_info['full_public_name']
                        # generate some hopefully unique ids if they are 0
                        uid = person_info['id'] or (crc32(name.encode()) & 0xffffffff)
                        persons[uid] = name

                    links = {}
                    for link_info in talk.get('links', []):
                        title = link_info['title']
                        # generate some hopefully unique ids if they are 0
                        url = link_info['url']
                        links[url] = title

                    attachments = {}
                    for attachment_info in talk.get('attachments', []):
                        title = attachment_info['title']
                        # generate some hopefully unique ids if they are 0
                        url = attachment_info['url']
                        attachments[url] = title

                    day.add_event(room_name, Event(
                        uid=talk['id'],
                        date=parse_datetime(talk['date']),
                        start=parse_time(talk['start']),
                        duration=parse_duration(talk['duration']),
                        slug=talk['slug'],
                        title=talk['title'],
                        description=talk.get('description', ''),
                        abstract=talk.get('abstract', ''),
                        language=talk['language'],
                        persons=persons,
                        download_url=talk.get('download_url', ''),
                        recording_license=talk.get('recording_license', ''),
                        recording_optout=talk['do_not_record'],
                        subtitle=talk.get('subtitle', ''),
                        track=talk.get('track', ''),
                        event_type=talk.get('type', ''),
                        logo=talk.get('logo', ''),
                        links=links,
                        attachments=attachments
                    ))

        assert conference.day_count == conf_tree['daysCount']
        return schedule

