# This file is part of voctosched, a frab schedule converter.
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

import logging

from fahrplan.datetime import parse_date, parse_datetime, parse_duration, parse_time
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from fahrplan.slug import StandardSlugGenerator
from ..base import ImportHandler
from hacks import noexcept


class FakeImportHandler(ImportHandler):
    @noexcept(logging.getLogger(__name__))
    def run(self):
        conference = Conference(
            title="DENOG8",
            acronym="denog16",
            day_count=2,
            start=parse_date("2016-11-23"),
            end=parse_date("2016-11-24"),
            time_slot_duration=parse_duration("00:10")
        )
        slug = StandardSlugGenerator(conference)
        schedule = Schedule(conference=conference)
        schedule.add_room("darmstadtium")
        schedule.add_event(1, "darmstadtium", Event(
            uid=4001, date=parse_datetime("2016-11-23T13:00:00"),
            start=parse_time("13:00"), duration=parse_duration("00:15"),
            slug=slug, title="Opening", language="en", persons={1: "DENOG ORGA"}
        ))
        schedule.add_event(2, "darmstadtium", Event(
            uid=4002, date=parse_datetime("2016-11-24T19:00:00"),
            start=parse_time("19:00"), duration=parse_duration("00:15"),
            slug=slug, title="Closing", language="en", persons={1: "DENOG ORGA"}
        ))
        return schedule
