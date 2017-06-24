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

from fahrplan.xml import XmlWriter, XmlSerializable
from .event import Event


class Room(XmlSerializable):
    def __init__(self, name: str):
        self.name = name
        self.events = dict()
        self.day = None

    def add_event(self, event: Event):
        event.room = self
        self.events[event.id] = event

    def get_start(self):
        try:
            return min(event.date for event in self.events.values())
        except ValueError:
            # No events assigned
            return None

    def get_end(self):
        try:
            return max(event.date + event.duration for event in self.events.values())
        except ValueError:
            # No events assigned
            return None

    def merge(self, other: 'Room'):
        for uid, event in other.events.items():
            if self.day.schedule.has_collision(event):
                continue
            self.add_event(event)

    def append_xml(self, xml: XmlWriter, extended: bool):
        with xml.context("room", name=self.name):
            for event in self.events.values():
                xml.append_object(event, extended)
