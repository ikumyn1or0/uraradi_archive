import copy
import csv
import dataclasses
import re
from typing import Union


from Class import Time


ADDITIONAL_GUESTS = {"2022-10-28": ["島村シャルロット", "宗谷いちか"]}
RECORDING_DATES = ["2023-03-10"]


@dataclasses.dataclass()
class Title:
    title: str

    def as_full(self):
        return self.title

    def as_number(self):
        if "総集編" in self.title:
            return self.title[8:15]
        if 2 <= self.title.count("【"):
            return re.search(r"^【\S+】", self.title).group()[4:-1]
        if 2 <= self.title.count("｜"):
            return re.search(r"｜\S+ 裏ラジ", self.title).group()[1:-4]
        raise Exception

    def as_shorten(self):
        if "総集編" in self.title:
            return self.title[0:8]
        if 2 <= self.title.count("【"):
            start_index = self.title.find("】") + 1
            end_index = self.title.rfind("【")
            if "裏ラジオウルナイト" in self.title[start_index: end_index]:
                end_index = self.title[0: end_index].rfind("裏ラジオウルナイト")
            if "/" in self.title[start_index: end_index]:
                end_index = self.title[0: end_index].rfind("/")
            return self.title[start_index: end_index].rstrip()
        if 2 <= self.title.count("｜"):
            start_index = 0
            end_index = self.title.find("｜")
            return self.title[start_index: end_index]
        raise Exception

    def extract_guests(self):
        if "総集編" in self.title:
            return []
        if 2 <= self.title.count("【"):
            casts_with_belongs = self.title[self.title.rfind("【"): self.title.rfind("】")]
            casts = casts_with_belongs[1: casts_with_belongs.find(" / ")]
            guests = [cast for cast in casts.split("・") if cast != "大浦るかこ"]
            return guests
        if 2 <= self.title.count("｜"):
            casts_with_belongs = self.title[self.title.rfind("｜"): self.title.rfind(" // ")]
            casts = casts_with_belongs[1:]
            guests = [cast for cast in casts.split(" / ") if cast != "大浦るかこ"]
            return guests
        raise Exception


@dataclasses.dataclass()
class Radio:
    date: str
    youtube_id: str
    title: Title
    length: Time.Time
    guests: list[str]
    is_clip: bool
    is_recording: bool

    def __init__(self, **args):
        self.date = args["date"]
        self.youtube_id = self.url_to_id(args["url"])
        self.title = Title(args["title"])
        self.length = Time.Time(args["length_s"])
        self.guests = self.title.extract_guests()
        if self.date in ADDITIONAL_GUESTS.keys():
            self.guests.extend(ADDITIONAL_GUESTS[self.date])
        self.is_clip = ("総集編" in args["title"])
        self.is_recording = (args["date"] in RECORDING_DATES)

    def url_to_id(self, url: str) -> str:
        ID_LENGTH = 11
        patterns_before_id = ["youtube.com/watch?v=",
                              "youtube.com/live/"]
        for pattern in patterns_before_id:
            if pattern not in url:
                continue
            id_index = url.find(pattern) + len(pattern)
            return url[id_index: id_index + ID_LENGTH]
        raise Exception

    def get_url(self, timestamp: Union[str, None] = None) -> str:
        if timestamp is None:
            return f"https://youtu.be//{self.youtube_id}"
        else:
            return f"https://youtu.be//{self.youtube_id}?t={timestamp}"

    def get_thumbnail_url(self, quality="default"):
        if quality in ["hqdefault", "mqdefault", "sddefault", "maxresdefault"]:
            return f"http://img.youtube.com/vi/{self.youtube_id}/{quality}.jpg"
        else:
            return f"http://img.youtube.com/vi/{self.youtube_id}/default.jpg"

    def get_guests(self):
        return copy.deepcopy(self.guests)

    def get_length(self):
        return copy.deepcopy(self.length)


@dataclasses.dataclass()
class RadioList:
    radios: dict[str, Radio] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        with open("inputs/playlist_裏ラジオウルナイト.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row["date"]
                self.radios[date] = Radio(**row)

    def get_dates(self, ascending=False):
        return sorted(list(self.radios.keys()), reverse=not ascending)

    def get_radios(self, date_ascending=False):
        return sorted(list(self.radios.items()), key=lambda x: x[0], reverse=not date_ascending)

    def get_radio_in(self, date):
        return self.radios[date]

    def get_total_num(self):
        return len(self.radios)

    def get_total_guests_num(self):
        guests = []
        for date, radio in self.get_radios():
            guests.extend(radio.get_guests())
        return len(set(guests))

    def get_total_length(self):
        time_list = [radio.get_length() for date, radio in self.get_radios()]
        return Time.sum_time(time_list)

    def get_average_length(self):
        time_list = [radio.get_length() for date, radio in self.get_radios() if not radio.is_clip and not radio.is_recording]
        return Time.average_time(time_list)

    def get_total_guests(self):
        guests = []
        for radio in self.radios.values():
            guests.extend(radio.get_guests())
        return list(set(guests))
