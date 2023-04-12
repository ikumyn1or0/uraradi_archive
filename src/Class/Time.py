import dataclasses
import datetime


@dataclasses.dataclass()
class Time:
    time_s: int

    def __init__(self, time_s: str):
        self.time_s = int(time_s)

    def as_second(self) -> int:
        return self.time_s

    def as_hour(self) -> float:
        return self.time_s / 3600

    def as_hms(self, ja_style=False) -> str:
        abs_time_s = abs(self.time_s)
        seconds = abs_time_s % 60
        minutes = int(abs_time_s / 60) % 60
        if ja_style:
            hms = str(minutes).zfill(2) + "分" + str(seconds).zfill(2) + "秒"
        else:
            hms = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        if 1 <= abs_time_s / 3600:
            hours = int(abs_time_s / 3600) % 24
            if ja_style:
                hms = str(hours).zfill(2) + "時間" + hms
            else:
                hms = str(hours).zfill(2) + ":" + hms
        if 1 <= abs_time_s / 86400:
            days = int(abs_time_s / 86400)
            if ja_style:
                hms = str(days) + "日" + hms
            else:
                hms = str(days) + ":" + hms
        if self.time_s < 0:
            hms = "-" + hms
        return hms

    def as_datetime(self, year=1900, month=1, day=1):
        abs_time_s = abs(self.time_s)
        seconds = abs_time_s % 60
        minutes = int(abs_time_s / 60) % 60
        hours = int(abs_time_s / 3600) % 24
        days = int(abs_time_s / 86400)
        return datetime.datetime(year=year,
                                 month=month,
                                 day=day + days,
                                 hour=hours,
                                 minute=minutes,
                                 second=seconds)


def sum_time(time_list):
    return Time(sum([time.time_s for time in time_list]))


def average_time(time_list):
    return Time(int(sum([time.time_s for time in time_list]) / len(time_list)))
