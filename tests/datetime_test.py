import unittest
import datetime as dt
from fahrplan.datetime import format_duration


class TestFormatDuration(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_duration(dt.timedelta()), "00:00")

    def test_hours_and_minutes(self):
        self.assertEqual(format_duration(dt.timedelta(hours=2, minutes=30)), "02:30")

    def test_more_than_24_hours(self):
        self.assertEqual(format_duration(dt.timedelta(hours=27, minutes=15)), "27:15")


if __name__ == "__main__":
    unittest.main()
