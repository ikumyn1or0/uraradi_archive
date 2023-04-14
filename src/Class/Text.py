import copy
import csv
import dataclasses
import glob


from Class import Time


@dataclasses.dataclass()
class Sentence:
    timestamp_start: Time.Time
    timestamp_end: Time.Time
    text: str

    def __init__(self, **args):
        self.timestamp_start = Time.Time(args["start_s"])
        self.timestamp_end = Time.Time(args["end_s"])
        self.text = args["text"]

    def get_timestamp_start(self):
        return copy.deepcopy(self.timestamp_start)

    def get_text(self):
        return copy.deepcopy(self.text)


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

    def get_sentences(self, timestamp_ascnding=True):
        return sorted(self.sentences, key=lambda x: x.timestamp_start.as_second(), reverse=not timestamp_ascnding)


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
            self.transcripts[date] = None

    def get_dates(self, ascending=False):
        return sorted(list(self.transcripts.keys()), reverse=not ascending)

    def get_transcript_in(self, date):
        if self.transcripts[date] is None:
            self.transcripts[date] = Transcript(date)
        return self.transcripts[date]


@dataclasses.dataclass()
class Comment:
    timestamp: Time.Time
    text: str

    def __init__(self, **args):
        self.timestamp = Time.Time(args["start_s"])
        self.text = args["text"]

    def get_timestamp(self):
        return copy.deepcopy(self.timestamp)

    def get_text(self):
        return copy.deepcopy(self.text)


@dataclasses.dataclass()
class Chat:
    date: str
    comments: list[Comment]

    def __init__(self, date):
        self.date = date
        self.comments = []
        with open(f"inputs/chats/{date}.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.comments.append(Comment(**row))

    def get_comments(self, timestamp_ascnding=True):
        return sorted(self.comments, key=lambda x: x.timestamp.as_second(), reverse=not timestamp_ascnding)


@dataclasses.dataclass()
class ChatList:
    chats: dict[str, Chat] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        paths = glob.glob("inputs/chats/*.csv")
        dates = []
        for path in paths:
            filename = path.split("/")[-1]
            date = filename.split(".")[0]
            dates.append(date)
        for date in dates:
            self.chats[date] = None

    def get_dates(self, ascending=False):
        return sorted(list(self.chats.keys()), reverse=not ascending)

    def get_chat_in(self, date):
        if self.chats[date] is None:
            self.chats[date] = Chat(date)
        return self.chats[date]
