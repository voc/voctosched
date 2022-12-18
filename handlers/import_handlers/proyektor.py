import json
import logging

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

        slug = StandardSlugGenerator(conference)
        schedule = Schedule(conference=conference)
        rec_license = self.global_config.get('conference', 'license')
        day0 = parse_date(self.global_config.get('conference', 'start'))

        for b in tree:
            # filter for locations we want to import
            #if b['genre'] not in ['Lecture', 'Workshop', 'Podium', 'Talk']:  # todo move to config
            #    continue
            # one event (booking) can have multiple shows in proyektor. Most likely we will only have on per talk.
            # We need to look into all as the room (stage) is child of a show and we want to filter stages
            for show in b['shows']:
                #if show['stage'] not in ['Content', 'Oase', 'Workshop-Hanger']:  # todo move to config
                #    continue

                start = parse_datetime(show['start'])
                end = parse_datetime(show['end'])
                day = (start.date() - day0).days + 1

                duration = end - start
                # build a description the dirty way. currently we don't know how many languages are possible
                description = ""
                if b.get('description_de'):
                    description += b.get('description_de')
                if b.get('description_en'):
                    if len(description) == 0:
                        description += b.get('description_en')
                    else:
                        description += "\n\n\n" + b.get('description_en')

                if "Language: EN" in description or "Language:EN" in description:
                    language = "en"
                elif "Language: DE" in description or "Language:DE" in description:
                    language = "de"
                else:
                    language = ""

                if "Recording: Yes" in description or "Recording:Yes" in description:
                    rec_optout = False
                else:
                    rec_optout = True

                if b.get('artist_name'):
                    title = b.get('artist_name')
                else:
                    title = b['program_name']

                if not title:
                    continue

                if b.get('program_name'):
                    persons_names = [x.strip() for x in b['program_name'].split(',')]
                    persons = dict(zip(range(len(persons_names)), persons_names))
                else:
                    persons = {}

                event = Event(
                    uid=b['booking_id'],
                    date=start,
                    start=start.time(),
                    duration=duration,
                    slug=slug,
                    title=title,
                    description=description.strip('\n'),
                    language=language,
                    persons=persons,
                    recording_license=rec_license,
                    recording_optout=rec_optout,
                    event_type=b['genre']
                )

                schedule.add_room(show['stage'])
                schedule.add_event(day, show['stage'], event)

        return schedule
