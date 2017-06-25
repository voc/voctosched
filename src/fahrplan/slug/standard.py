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

import codecs
import re
import translitcodec
from string import ascii_letters, digits

from fahrplan.model.conference import Conference
from fahrplan.model.event import Event


class StandardSlugGenerator:
    def __init__(self, conference: Conference):
        self.acronym = conference.acronym

    def __call__(self, event: Event):
        title = StandardSlugGenerator.normalize_name(event.title)
        return f"{self.acronym}-{event.id}-{title}"[:240]

    @staticmethod
    def normalize_name(name: str):
        name = codecs.encode(name, 'translit/long')
        name = re.sub(r"\W+", "_", name)
        legal_chars = ascii_letters + digits + "_"
        pattern = f"[^{legal_chars}]+"
        name = re.sub(pattern, "", name)
        name = name.lower()
        return name
