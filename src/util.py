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

from typing import Union


log = logging.getLogger(__name__)


def write_file(path: str, content: str) -> bool:
    log.info(f'Writing file "{path}".')
    try:
        with open(path, "w") as f:
            f.write(content)
        return True
    except PermissionError:
        log.error(f'No permission to open "{path}".')
        return False
    except IsADirectoryError:
        log.error(f'Cannot open directory "{path}".')
        return False
    except IOError:
        log.exception(f'Error writing file "{path}".')
        return False


def read_file(path: str) -> Union[str, None]:
    log.info(f'Reading file "{path}".')
    try:
        with open(path, "r") as f:
            content = f.read()
        return content
    except PermissionError:
        log.error(f'No permission to open "{path}".')
        return None
    except IsADirectoryError:
        log.error(f'Cannot open directory "{path}".')
        return None
    except IOError:
        log.exception(f'Error reading file "{path}".')
        return None
