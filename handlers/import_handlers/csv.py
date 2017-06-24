# This file is part of voctosched, a frab schedule converter.
# Copyright (C) 2017-2017 derpeter <derpeter@berlin.ccc.de>
# Copyright (C) 2017-2017 Markus Otto <otto@fs.tum.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
                schedule.add_room(row['Room'])
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
                    persons={row['SpeakerID']: row['Speaker']},
                    download_url=row.get('File URL', ''),
                    recording_license=rec_license
                ))

        return schedule

