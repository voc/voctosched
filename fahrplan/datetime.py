import datetime as dt

from .exception import FahrplanError

TIME_FORMAT = "%H:%M"


def format_datetime(datetime: dt.datetime) -> str:
    return datetime.isoformat()


def parse_datetime(date_string: str) -> dt.datetime:
    return dt.datetime.fromisoformat(date_string)


def format_date(date: dt.date) -> str:
    return str(date)


def parse_date(date_string: str) -> dt.date:
    try:
        items = [int(i, 10) for i in date_string.split("-")]
        return dt.date(*items)

    except (TypeError, ValueError):
        raise FahrplanError(f"{date_string} is not in required format %Y-%m-%d")


def _parse_time_items(time_string: str) -> list[int]:
    try:
        if '.' in time_string:  # ...just drop miliseconds.
            time_string = time_string[:time_string.index('.')]

        return [int(i, 10) for i in time_string.split(":")]
    except ValueError:
        raise FahrplanError(f"{time_string} is not in required format %H:%M[:%S]")


def format_time(time: dt.time) -> str:
    return time.strftime(TIME_FORMAT)


def parse_time(time_string: str) -> dt.time:
    return dt.time(*_parse_time_items(time_string))


def format_duration(duration: dt.timedelta) -> str:
    # just cut away the seconds part
    return str(duration)[:-3]


def parse_duration(duration_string: str) -> dt.timedelta:
    items = _parse_time_items(duration_string)
    seconds = items[2] if len(items) >= 3 else 0
    return dt.timedelta(hours=items[0], minutes=items[1], seconds=seconds)
