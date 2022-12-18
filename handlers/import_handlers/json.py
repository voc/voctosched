import json
import logging

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_duration
from fahrplan.model.conference import Conference
from fahrplan.model.day import Day
from fahrplan.model.event import Event
from fahrplan.model.room import Room
from fahrplan.model.schedule import Schedule
from hacks import noexcept
from util import read_input


log = logging.getLogger(__name__)


class JSONImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        # import json file to dict tree
        tree = json.loads(read_input(self.config['path']))

        # handy references to subtrees
        sched = tree['schedule']
        con = tree['schedule']['conference']

        # create the conference object
        conference = Conference(
            title=con['title'],
            acronym=con['acronym'],
            day_count=0,  # do not automatically generate days
            start=parse_date(con['start']),
            end=parse_date(con['end']),
            time_slot_duration=parse_duration(con['timeslot_duration'])
        )

        schedule = Schedule(conference=conference, version=sched['version'])

        for room in con['rooms']:
            conference.add_room(Room.from_dict(room))

        for day_tree in con['days']:
            day = Day.from_dict(day_tree)
            schedule.add_day(day)

            for room_name, room_talks in day_tree['rooms'].items():
                day.add_room(Room(room_name))

                for talk in room_talks:
                    day.add_event(room_name, Event.from_dict(talk))

        assert conference.day_count == con['daysCount']
        return schedule

