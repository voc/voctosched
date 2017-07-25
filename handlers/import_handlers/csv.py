import binascii
import csv
import logging

from io import StringIO

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_time, parse_datetime, parse_duration
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from fahrplan.slug import StandardSlugGenerator
from hacks import noexcept
from util import read_file


log = logging.getLogger(__name__)


class CSVImportHandler(ImportHandler):
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

        content = read_file(self.config['path'])
        with StringIO(content) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                room = row['Room']
                if room != "import":
                    log.debug("Event not marked for import, skipping")
                    continue

                schedule.add_room(room)

                uid = row['ID']
                log.debug(f'Handling event {uid}')

                speakers = {}
                for speaker in row['Speakers'].split(','):
                    if not speaker:
                        continue
                    speaker = speaker.strip()
                    speaker_id = binascii.crc32(speaker.encode())
                    speakers[int(speaker_id)] = speaker
                if not speakers:
                    speakers = {2053352521: "no_name"}

                day_map = {
                    "2017-07-01": "1",  # TODO is this ok?
                    "2017-07-04": "1",
                    "2017-07-05": "2",
                    "2017-07-06": "3",
                    "2017-07-07": "4",
                    "2017-07-08": "5",
                    "2017-07-09": "6",
                }
                date = row['Date']
                day = day_map[date]
                start = "04:00"
                duration = "0:30"

                schedule.add_event(int(day), room, Event(
                    uid=uid,
                    date=parse_datetime(date + 'T' + start + ':00'),
                    start=parse_time(start),
                    duration=parse_duration(duration),
                    slug=slug,
                    title=row['Title'],
                    description=row.get('Description', ''),
                    abstract=row.get('Abstract', ''),
                    language=row['Language'],
                    persons=speakers,
                    download_url=f"/video/fcmc17/fcmc/publish_ready/video/already_sent{row.get('File URL', '')}",
                    recording_license=rec_license
                ))

        return schedule

