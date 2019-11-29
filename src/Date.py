from datetime import datetime


class Date:

    def __init__(self, time):
        self.time = time

    def plus_hour(self, value):
        hour = self.time.hour
        day = self.time.day
        if self.time.hour + value > 23:
            hour = 0
            day = self.get_day(value)
        else:
            hour += value

        return datetime(self.time.year, self.time.month, day, hour, self.time.minute, self.time.second,
                        self.time.microsecond)

    def get_day(self, value):
        if self.time.day + value > 31:
            return 1 + value
        if self.time.month == 2:
            if self.is_leap_year():
                if self.time.day + value > 29:
                    return 1 + value
            else:
                if self.time.day + value > 28:
                    return 1 + value
        elif self.time.month % 2 == 0 and self.time.day > 30:
            return 1 + value
        else:
            return self.time.day + value

    def is_leap_year(self):
        return (self.time.year % 4 == 0 and self.time.year % 400 == 0) or (
                self.time.year % 4 == 0 and self.time.year % 100 != 0)
