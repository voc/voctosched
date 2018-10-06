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
from util import read_input


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

        content = read_input(self.config['path'])
        with StringIO(content) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                if row['Room'] == '' and row['ID'] == '' and row['Title'] == '':
                    continue

                schedule.add_room(row['Room'])
                speakers = {}
                for pair in row['Speakers'].split('|'):
                    uid, _, name = pair.partition(":")
                    speakers[int(uid)] = name
                schedule.add_event(int(row['Day']), row['Room'], Event(
                    uid=row['ID'],
                    date=parse_datetime(row['Date'] + 'T' + row['Start'] + ':00'),
                    start=parse_time(row['Start']),
                    duration=parse_duration(row['Duration']),
                    slug=slug,
                    title=row['Title'],
                    description=row.get('Description', ''),
                    abstract=row.get('Abstract', ''),
                    language=row['Language'],
                    persons=speakers,
                    download_url=row.get('File URL', ''),
                    recording_license=rec_license
                ))

        return schedule

