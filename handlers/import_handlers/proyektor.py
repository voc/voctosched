import json
import logging
import datetime

from io import StringIO
from pprint import pprint

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_time, parse_datetime, parse_duration
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from fahrplan.slug import StandardSlugGenerator
from hacks import noexcept
from util import read_file


log = logging.getLogger(__name__)

class ProyektorImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        # create the conference object
        conference = Conference(
            title=self.global_config.get('conference', 'title'),
            acronym=self.global_config.get('conference', 'acronym'),
            day_count=int(self.global_config.get('conference', 'day_count')),
            start=parse_date(self.global_config.get('conference', 'start')),
            end=parse_date(self.global_config.get('conference', 'end')),
            time_slot_duration=parse_duration(self.global_config.get('conference', 'time_slot_duration'))
        )
        slug = StandardSlugGenerator(conference)
        schedule = Schedule(conference=conference)
        rec_license = self.global_config.get('conference', 'license')

        day0 = datetime.datetime(2018, 6, 26)

        with open(self.config['path'], "r") as read_file:
            parsed_json = json.load(read_file)

            for row in parsed_json:
                if row['floor'] not in ['Theater', 'Workshop Hangar']:
                    continue

                start = parse_datetime(row['start'][:19])
                end = parse_datetime(row['end'][:19])
                day =  abs(start.date() - day0.date()).days
                duration = end - start

                event = Event(
                    uid=row['showId'].replace('_', '00'),  # underscore raus machen
                    date=start,
                    start=start.time(),
                    duration=duration,
                    slug=slug,
                    title=row['artist'],
                    description=row.get('genre'),
                    language='EN',
                    persons={'0':' '}
                )

                schedule.add_room(row['floor'])
                schedule.add_event(day, row['floor'], event)

        return schedule
