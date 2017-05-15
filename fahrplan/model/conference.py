from datetime import date
from datetime import timedelta


class Conference:
    def __init__(self, title: str, acronym: str, days: int, start: date, end: date, timeslot_duration: timedelta):
        self.title = title
        self.acronym = acronym
        self.days = days
        self.start = start
        self.end = end
        self.timeslot_duration = timeslot_duration
