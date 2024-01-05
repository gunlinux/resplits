import os
from jinja2 import Template
from dataclasses import dataclass
from datetime import datetime
from bs4 import Tag


DATE_FORMAT = '%m/%d/%Y %H:%M:%S'
TPL_DIR = 'tpls'


def render_tpl(tpl, **kwargs):
    with open(os.path.join(TPL_DIR, tpl)) as file:
        template = Template(file.read())
    return template.render(**kwargs)


@dataclass
class RunTime:
    id: int = None
    Realtime: str = ''
    Gametime: str = ''

    def __init__(self, bs=None):
        if bs is None:
            return

        for child in bs.children:
            if not child.name:
                continue
            if child.name.lower() == 'realtime':
                self.Realtime = child.contents[0]
            if child.name.lower() == 'gametime':
                self.Gametime = child.contents[0]
        if bs.attrs:
            id_from_bs = bs.attrs.get('id', None)
            if id_from_bs:
                self.id = int(id_from_bs)


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
class Segment:
    name: str = ''
    icon: str = ''
    # splittime: afterparty
    bestsegmenttime: RunTime = None
    segmentshistory = list[RunTime]

    def __init__(self, bs=None):
        if bs is None:
            return
        for child in bs.children:
            if isinstance(child, Tag):
                if child.name.lower() == 'name' and child.contents:
                    self.name = child.contents[0]
                if child.name.lower() == 'icon' and child.contents:
                    self.icon = child.contents[0]
                if child.name.lower() == 'bestsegmenttime' and child.contents:
                    self.bestsegmenttime = RunTime(child)
                if child.name.lower() == 'segmenthistory':
                    self.segmentshistory = self.__get_segments_history(child)

    def __find(self, bs, name):
        tag = bs.find(name)
        if not tag or not tag.contents:
            return None
        return tag.contents[0]

    def __get_segments_history(self, bs):
        runtimes = []
        for child in bs.children:
            if child == '\n':
                continue
            runtime = RunTime(child)
            runtimes.append(runtime)
        return runtimes


@dataclass
class Run:
    offset: str
    attempt_count: int
    attempt_history: list[Attempt]
    segments: list[Segment]
    game_icon: str = ''
    game_name: str = ''
    category_name: str = ''
    layout_path: str = ''
    # TODO ADD PB

    def __init__(self, bs=None):
        if not bs:
            return
        bsrun = bs.Run
        self.game_icon = self.__load_value(bsrun.GameIcon, '')
        self.game_name = self.__load_value(bsrun.GameName)
        self.category_name = self.__load_value(bsrun.CategoryName)
        self.layout_path = self.__load_value(bsrun.LayoutPath)
        self.offset = self.__load_value(bsrun.Offset)
        self.attempt_count = self.__load_value(bsrun.AttemptCount)
        self.attempt_history = self.__load_attemtps(bsrun.AttemptHistory)
        self.segments = self.__load_segments(bsrun.segments)

    def __load_value(self, value, default=None):
        if not value or not value.contents:
            return default
        return value.contents[0]

    def __load_attemtps(self, bs):
        attempts = []
        for child in bs.children:
            if hasattr(child, 'attrs'):
                attempt = Attempt(child)
                attempts.append(attempt)
        return attempts

    def __load_segments(self, bs):
        segments = []
        for child in bs.children:
            if child == '\n':
                continue
            segment = Segment(child)

            segments.append(segment)
        return segments

    def render(self):
        segments = render_tpl('segments.tpl', segments=self.segments)
        attempt_history = render_tpl('attempt_history.tpl',
                                     attempts=self.attempt_history)
        return render_tpl('run.tpl', obj=self, segments=segments,
                          attempt_history=attempt_history)

    @property
    def segments_count(self):
        return len(self.segments)
