from dataclasses import dataclass
from datetime import datetime
DATE_FORMAT = '%m/%d/%Y %H:%M:%S'


@dataclass
class RunTime:
    Realtime: str = ''
    Gametime: str = ''

    def __init__(self, bs=None):
        if bs is None:
            return

        for child in bs.children:
            if child.name == 'RealTime':
                self.Realtime = child.contents[0]
            if child.name == 'GameTime':
                self.Gametime = child.contents[0]


@dataclass
class Attempt:
    id: int
    started: datetime
    ended: datetime
    isEndedSynced: False
    isStartedSynced: True
    runtime: RunTime = None

    def __init__(self, bs=None):
        if bs is None:
            print('DANILA A U CRAZY')
            return
        self.id = int(bs.attrs.get('id'))
        if bs.contents:
            self.runtime = RunTime(bs)
        self.started = datetime.strptime(bs.attrs.get('started'), DATE_FORMAT)
        self.ended = datetime.strptime(bs.attrs.get('ended'), DATE_FORMAT)
        self.isStartedSynced = 'True' == bs.attrs.get('isStartedSynced', False)
        self.isEndedSynced = 'True' == bs.attrs.get('isEndedSynced', False)


@dataclass
class Run:
    GameIcon: str
    GameName: str
    CategoryName: str
    LayoutPath: str
    Offset: str
    AttemptCount: int
    AttemptHistory: list[Attempt]

    def __init__(self, bs=None):
        if not bs:
            return
        bsrun = bs.Run
        self.GameIcon = self.__load_value(bsrun.GameIcon)
        self.GameName = self.__load_value(bsrun.GameName)
        self.CategoryName = self.__load_value(bsrun.CategoryName)
        self.LayoutPath = self.__load_value(bsrun.LayoutPath)
        self.Offset = self.__load_value(bsrun.Offset)
        self.AttemptCount = self.__load_value(bsrun.AttemptCount)
        self.AttemptHistory = self.__load_attemtps(bsrun.AttemptHistory)

    def __load_value(self, value):
        if not value or not value.contents:
            print(f'not value {value}')
            return None
        return value.contents[0]

    def __load_attemtps(self, bs):
        attempts = []
        for child in bs.children:
            if hasattr(child, 'attrs'):
                attempt = Attempt(child)
                attempts.append(attempt)
        print(attempts)
        return attempts
