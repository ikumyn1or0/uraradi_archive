import csv
import dataclasses
import glob


import Time


@dataclasses.dataclass()
class Text:
    text: str


@dataclasses.dataclass()
class Sentence:
    timestamp_start: Time.Time
    timestamp_end: Time.Time
    sentence: Text

    def __init__(self, **args):
        self.timestamp_start = Time.Time(args["start_s"])
        self.timestamp_end = Time.Time(args["end_s"])
        self.sentence = Text(args["text"])


@dataclasses.dataclass()
class Transcript:
    date: str
    sentences: list[Sentence]

    def __init__(self, date):
        self.date = date
        self.sentences = []
        with open(f"inputs/transcripts/{date}.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.sentences.append(Sentence(**row))


@dataclasses.dataclass()
class TranscriptList:
    transcripts: dict[str, Transcript] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        paths = glob.glob("inputs/transcripts/*.csv")
        dates = []
        for path in paths:
            filename = path.split("/")[-1]
            date = filename.split(".")[0]
            dates.append(date)
        for date in dates:
            self.transcripts[date] = Transcript(date)
