import os
import copy
from jinja2 import Template
from dataclasses import dataclass
from datetime import datetime, timedelta
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

    def get_gametime(self):
        return Run.get_msecs(self.Gametime)


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
    split_times: dict[str, RunTime]
    segmentshistory: list[RunTime] = None
    name: str = ''
    icon: str = ''
    bestsegmenttime: RunTime = None

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
                if child.name.lower() == 'splittimes':
                    self.split_times = self.__get_splittimes(child)

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

    def __get_splittimes(self, bs):
        split_times = {}
        for child in bs.children:
            if not isinstance(child, Tag):
                continue
            name = child.attrs.get('name', None)
            runtime = RunTime(child)
            if name:
                split_times[name] = runtime
        return split_times


@dataclass
class Run:
    name: str
    offset: str
    attempt_count: int
    attempt_history: list[Attempt]
    segments: list[Segment]
    levels: list[str]
    game_icon: str = ''
    game_name: str = ''
    category_name: str = ''
    # TODO ADD PB
    updated: bool = False

    def __init__(self, bs=None, name=''):
        if not bs:
            return
        bsrun = bs.Run
        if name:
            self.name = name
        self.game_icon = self.__load_value(bsrun.GameIcon, '')
        self.game_name = self.__load_value(bsrun.GameName)
        self.category_name = self.__load_value(bsrun.CategoryName)
        self.layout_path = self.__load_value(bsrun.LayoutPath)
        self.offset = self.__load_value(bsrun.Offset)
        self.attempt_count = self.__load_value(bsrun.AttemptCount)
        self.attempt_history = self.__load_attemtps(bsrun.AttemptHistory)
        self.segments = self.__load_segments(bsrun.Segments)
        self.get_levels()

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

    def get_levels(self):
        self.levels = []
        for segment in self.segments:
            if segment.name.startswith('C'):
                self.levels.append(segment.name)

    def get_level_pb(self, name):
        # get full level personal best time
        runs = {}
        calc = {}
        for segment in self.segments:
            if segment.name.startswith(f'-{name}_') or segment.name == name:
                for time in segment.segmentshistory:
                    if runs.get(time.id):
                        runs[time.id] += time.get_gametime()
                    else:
                        runs[time.id] = time.get_gametime()
                    calc[time.id] = calc[time.id] + 1 if calc.get(time.id) else 1

        filtered = []
        for k,  v in runs.items():
            if calc[k] < max(calc.values()):
                continue
            filtered.append(v)
        return self.msecs_to_str(min(filtered))

    def get_level_bs(self, name):
        # get full level GOLDTIME
        gold = 0
        for segment in self.segments:
            if segment.name.startswith(f'-{name}_') or segment.name == name:
                gold += segment.bestsegmenttime.get_gametime()
        return gold


    def get_levels_pb(self):
        return {level: self.get_msecs(self.get_level_pb(level)) for level in self.levels}

    def get_levels_golds(self):
        return {level: self.get_level_bs(level) for level in self.levels}

    def render(self):
        segments = render_tpl('segments.tpl', segments=self.segments)
        attempt_history = render_tpl('attempt_history.tpl',
                                     attempts=self.attempt_history)
        return render_tpl('run.tpl', obj=self, segments=segments,
                          attempt_history=attempt_history)

    def save_to_file(self, path):
        print(f'saving to file {path}')
        render = self.render()
        with open(path, 'w') as f:
            f.write(render)

    @property
    def segments_count(self):
        return len(self.segments)

    @staticmethod
    def get_msecs(time: str) -> int:
        if len(time) == 8:
            time = f'{time}.0000000'
        temp = datetime.strptime(time[:15], '%H:%M:%S.%f')
        microseconds = (temp.hour*60*60 + temp.minute*60 + temp.second)*1_000_000 + temp.microsecond
        return microseconds

    @staticmethod
    def msecs_to_str(msecs: int) -> str:
        return str(timedelta(microseconds=msecs))


def get_chapter(run: Run, name:str):
    new_run = copy.deepcopy(run)
    new_run.attempt_history = []
    new_segments = []
    for segment in new_run.segments:
        if segment.name.startswith(f'-{name}_') or segment.name == name:
            new_segments.append(segment)
    new_run.segments = new_segments
    if name != 'C1':
        load_segment = copy.deepcopy(new_run.segments[0])
        load_segment.name = f'-{name}_load'
        load_segment.bestsegmenttime.Gametime = '00:00:00.0000000'
        new_run.segments.insert(0, load_segment)
    for segment in new_run.segments:
        segment.segmentshistory = []
        segment.splittimes = {}
        segment.split_times = {}
    new_run.save_to_file(f'{name}.lss')
    return new_run


