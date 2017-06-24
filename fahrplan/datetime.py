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

import datetime as dt

from .exception import FahrplanError

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
TIME_FORMAT = "%H:%M"


def format_datetime(datetime: dt.datetime):
    return datetime.strftime(DATETIME_FORMAT)


def parse_datetime(date_string: str):
    return dt.datetime.strptime(date_string, DATETIME_FORMAT)


def format_time(time: dt.time):
    return time.strftime(TIME_FORMAT)


def parse_time(time_string: str):
    try:
        hours, _, minutes = time_string.partition(":")
        hours = int(hours, 10)
        minutes = int(minutes, 10)
        return dt.time(hours, minutes)
    except ValueError:
        raise FahrplanError(f"{time_string} is not in required format %H:%M")


def format_date(date: dt.date):
    return str(date)


def parse_date(date_string: str):
    try:
        items = [int(i, 10) for i in date_string.split("-")]
        return dt.date(*items)

    except (TypeError, ValueError):
        raise FahrplanError(f"{date_string} is not in required format %Y-%m-%d")


def format_duration(duration: dt.timedelta):
    # just cut away the seconds part
    return str(duration)[:-3]


def parse_duration(duration_string: str):
    try:
        hours, _, minutes = duration_string.partition(":")
        hours = int(hours, 10)
        minutes = int(minutes, 10)
        return dt.timedelta(hours=hours, minutes=minutes)
    except ValueError:
        raise FahrplanError(f"{duration_string} is not in required format %H:%M")
