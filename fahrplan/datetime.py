import datetime as dt

from .exception import FahrplanError

TIME_FORMAT = "%H:%M"


def format_datetime(datetime: dt.datetime):
    return datetime.isoformat()


def parse_datetime(date_string: str):
    return dt.datetime.fromisoformat(date_string)


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
