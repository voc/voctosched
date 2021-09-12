import json
import logging
import datetime as dt

from pytz import timezone

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_time, parse_duration
from fahrplan.exception import FahrplanError
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from fahrplan.slug import StandardSlugGenerator
from hacks import noexcept


log = logging.getLogger(__name__)


class IndicoImportHandler(ImportHandler):
    """Imports data from Indico JSON exports.

    See https://docs.getindico.io/en/latest/http-api/ for more info.
    """

    @noexcept(log)
    def run(self) -> Schedule:
        if 'path' not in self.config:
            raise Error('Path to exported Indico JSON must be provided in the config file.')

        with open(self.config['path']) as f:
            indico_json = json.load(f)['results'][0]

        conference = Conference(
            title=self.global_config.get('conference', 'title'),
            acronym=self.global_config.get('conference', 'acronym'),
            day_count=int(self.global_config.get('conference', 'day_count')),
            start=parse_date(self.global_config.get('conference', 'start')),
            end=parse_date(self.global_config.get('conference', 'end')),
            time_slot_duration=parse_duration(self.global_config.get('conference', 'time_slot_duration'))
        )

        schedule = Schedule(conference=conference)
        language = self.global_config.get('conference', 'language')
        license = self.global_config.get('conference', 'license')
        fallback_speakers = {
            0: self.global_config.get('conference', 'fallback_speaker')
        }

        slugifier = StandardSlugGenerator(conference)

        for co in indico_json['contributions']:
            start_dt = self.parse_indico_date(co['startDate'])
            room = co['roomFullname'] or co['room'] or co['location'] or "Unknown"
            day = (start_dt.date() - conference.start).days + 1

            event = Event(
                uid=co['friendly_id'],
                date=start_dt,
                start=start_dt.time(),
                duration=dt.timedelta(minutes=co['duration']),
                title=co['title'].strip(),
                language=language,
                slug=slugifier,
                persons=self.collect_speakers(
                    fallback_speakers,  # In case there's nobody defined here...

                    # Coauthors are generally not speakers. Event metadata is often
                    # broken and has primary authors only, no speakers, so combine
                    # these and force uniqueness:
                    *co['speakers'],
                    *co['primaryauthors'],
                ),

                description=co['description'].strip(),
                links={"Indico Contribution Page": co['url']},
                recording_license=license,

                # Indico has this swapped around:
                track=co['session'] or "",
                event_type=co['track'] or "",
            )

            schedule.add_room(room)
            schedule.add_event(day, room, event)

        return schedule

    @staticmethod
    def parse_indico_date(indico_date: dict) -> dt.datetime:
        try:
            date = parse_date(indico_date['date'])
            time = parse_time(indico_date['time'])
            tz = timezone(indico_date['tz'])
            return dt.datetime.combine(date, time, tzinfo=tz)
        except ValueError:
            raise FahrplanError(f"{indico_date} is not a valid Indico date")

    @staticmethod
    def collect_speakers(fallback_speakers, *speakers) -> list[str]:
        # We can't just list(set([f"..." for s in speakers])) because
        # the native Python set is unordered and we need that.
        parsed = {}

        for s in speakers:
            if s['person_id'] not in parsed:
                parsed[s['person_id']] = f"{s['first_name'].strip()} {s['last_name'].strip()}"

        return parsed if len(parsed) > 0 else fallback_speakers
