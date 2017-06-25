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

import uuid as _uuid

# TODO (AK) rename to UUID_NAMESPACE as this is a global constant?
uuid_namespace = _uuid.UUID('54dc9c85-9b6a-40bd-9a36-41c004a5829b')


def uuid(uid, name):
    # TODO (AK) please document this method in detail and what the uuid namespace is for
    # TODO (AK) use format string for concatenation of name and uid
    # f"{name}{uid}"
    return str(_uuid.uuid5(uuid_namespace, str(name) + str(uid)))
