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

from logging import Logger, getLogger
from typing import Callable


def noexcept(log: Logger = getLogger(__name__)):
    """
    Grab all uncaught exceptions and log them with the logger
    of the module implementing the decorated function.
    :param log: logger of module using this.
    :return: False
    """
    def noexcept_decorator(f: Callable):
        def noexcept_inner(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return f(*args, **kwargs)
            except:
                log.exception("An unexpected error occurred.")
                return False
        return noexcept_inner

    if not isinstance(log, Logger) and callable(log):
        # probably was called without arguments
        actual_log = getLogger(__name__)
        actual_log.warning("\033[1;33mSome monkey used the noexcept decorator without arguments, "
                           "which should not have happened. Go bug the devs about it.\033[1;0m")
        return noexcept_decorator(log)
    return noexcept_decorator
