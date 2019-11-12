from datetime import datetime


class Date:

    def __init__(self, time):
        self.time = time

    def plus_hour(self, value):
        hour = self.time.hour
        day = self.time.day
        if self.time.hour + value > 23:
            hour = 0
            day = self.get_day()
        else:
            hour += value

        return datetime(self.time.year, self.time.month, day, hour, self.time.minute, self.time.second,
                        self.time.microsecond)

    def get_day(self):
        if self.time.day + 1 > 31:
            return 1
        elif self.time.month % 2 == 0 and self.time.day > 30:
            return 1
        else:
            return self.time.day + 1
