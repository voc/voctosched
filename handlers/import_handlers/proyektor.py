import json
import logging
import datetime

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_datetime, parse_duration
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from fahrplan.slug import StandardSlugGenerator
from hacks import noexcept
from util import read_input


log = logging.getLogger(__name__)


class ProyektorImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        # import json file to dict tree
        tree = json.loads(read_input(self.config['path']))

        # create the conference object
        conference = Conference(
            title=self.global_config.get('conference', 'title'),
            acronym=self.global_config.get('conference', 'acronym'),
            day_count=int(self.global_config.get('conference', 'day_count')),
            start=parse_date(self.global_config.get('conference', 'start')),
            end=parse_date(self.global_config.get('conference', 'end')),
            time_slot_duration=parse_duration(self.global_config.get('conference', 'time_slot_duration'))
        )

        schedule = Schedule(conference=conference)
        rec_license = self.global_config.get('conference', 'license')
        day0 = parse_date(self.global_config.get('conference', 'start'))

        for b in tree:
            # filter for locations we want to import
            if b['genre'] not in ['Lecture', 'Workshop', 'Podium']:  # todo move to config
                continue
            # one event (booking) can have multiple shows in proyektor. Most likely we will only have on per talk.
            # We need to look into all as the room (stage) is child of a show and we want to filter stages
            for show in b['shows']:
                if show['stage'] not in ['Content', 'Oase', 'Workshop-Hanger']:  # todo move to config
                    continue
                start = parse_datetime(show['start'][:19])
                end = parse_datetime(show['end'][:19])
                day = (start.date() - day0).days
                duration = end - start
                # build a description the dirty way. currently we dont know how many languages are possible
                description = ""
                if b['description_de']:
                    description += b['description_de']
                if b['description_en']:
                    if len(description) == 0:
                        description += b['description_en']
                    else:
                        description += "\n\n\n" + b['description_en']

                event = Event(
                    uid=b['booking_id'],
                    date=start,
                    start=start.time(),
                    duration=duration,
                    slug=show['name'].replace(" ", "_"),
                    title=show['name'],
                    description=description,
                    language='EN',  # we don't know that as the proyektor currently does not have that field
                    persons={0: b['artist_name']},
                    recording_license=rec_license,
                    event_type=b['genre']
                )

                schedule.add_room(show['stage'])
                schedule.add_event(day, show['stage'], event)

        return schedule
