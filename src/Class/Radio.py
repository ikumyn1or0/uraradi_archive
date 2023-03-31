import csv
import dataclasses
import re
from typing import Union


from Class import Time


ADDITIONAL_GUESTS = {"2022-10-28": ["島村シャルロット", "宗谷いちか"]}


@dataclasses.dataclass()
class Title:
    title: str

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
            guests = []
            for cast in casts.split("・"):
                if cast != "大浦るかこ":
                    guests.append(cast)
            return guests
        if 2 <= self.title.count("｜"):
            casts_with_belongs = self.title[self.title.rfind("｜"): self.title.rfind(" // ")]
            casts = casts_with_belongs[1:]
            guests = []
            for cast in casts.split(" / "):
                if cast != "大浦るかこ":
                    guests.append(cast)
            return guests
        raise Exception


@dataclasses.dataclass()
class Radio:
    date: str
    youtube_id: str
    title: Title
    length: Time.Time
    guests: list[str]

    def __init__(self, **args):
        self.date = args["date"]
        self.youtube_id = self.url_to_id(args["url"])
        self.title = Title(args["title"])
        self.length = Time.Time(args["length_s"])
        self.guests = self.title.extract_guests()
        if self.date in ADDITIONAL_GUESTS.keys():
            self.guests.extend(ADDITIONAL_GUESTS[self.date])

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


@dataclasses.dataclass()
class RadioList:
    radios: dict[str, Radio] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        with open("inputs/playlist_裏ラジオウルナイト.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row["date"]
                self.radios[date] = Radio(**row)