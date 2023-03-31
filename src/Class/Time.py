import dataclasses


@dataclasses.dataclass()
class Time:
    time_s: int

    def __init__(self, time_s: str):
        self.time_s = int(time_s)

    def as_second(self) -> int:
        return self.time_s

    def as_hour(self) -> float:
        return self.time_s / 3600

    def as_hms(self) -> str:
        abs_time_s = abs(self.time_s)
        seconds = abs_time_s % 60
        minutes = int(abs_time_s / 60) % 60
        hms = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        if 1 <= abs_time_s / 3600:
            hours = int(abs_time_s / 3600) % 24
            hms = str(hours).zfill(2) + ":" + hms
        if 1 <= abs_time_s / 86400:
            days = int(abs_time_s / 86400)
            hms = str(days) + ":" + hms
        if self.time_s < 0:
            hms = "-" + hms
        return hms
