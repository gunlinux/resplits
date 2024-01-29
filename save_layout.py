import os
import sys

from dotenv import load_dotenv
from ls import load_split
from models import Run

load_dotenv()
levels_path = 'lvls'


def load_levels(path, levels):
    runs = []
    for level in levels:
        level_run_soap = load_split(os.path.join(path, f'{level}.lss'))
        runs.append(Run(bs=level_run_soap, name=level))
    return runs


def update_main(mega,  runs: list[Run]):
    s = 0
    for run in runs:
        for segment in run.segments:
            bs = segment.bestsegmenttime.get_gametime()
            for main_segment in mega.segments:
                main_segment_bs = main_segment.bestsegmenttime
                if main_segment.name == segment.name and main_segment_bs.get_gametime() > bs:
                    segment_bs = segment.bestsegmenttime
                    print(f'{segment.name}  {main_segment_bs.Gametime} > {segment_bs.Gametime}')
                    s += main_segment_bs.get_gametime() - segment_bs.get_gametime()
                    main_segment.bestsegmenttime.Gametime = segment.bestsegmenttime.Gametime
    print(f'improved  main run time by {Run.msecs_to_str(s)}')
    return mega


def update_runs(mega,  runs: list[Run]):
    print('Updating  single  lines')
    s = 0
    for run in runs:
        for segment in run.segments:
            bs = segment.bestsegmenttime.get_gametime()
            for main_segment in mega.segments:
                main_segment_bs = main_segment.bestsegmenttime
                if main_segment.name == segment.name and main_segment_bs.get_gametime() < bs:
                    segment_bs = segment.bestsegmenttime
                    print(f'{segment.name}  {segment_bs.Gametime} > {main_segment_bs.Gametime}')
                    s += segment_bs.get_gametime() - main_segment.bestsegmenttime.get_gametime()
                    segment.bestsegmenttime.Gametime = main_segment.bestsegmenttime.Gametime
    print(f'improved  runs time by {Run.msecs_to_str(s)}')
    return runs


def main():
    mega_split_path = os.environ.get('mega_split')
    if not mega_split_path:
        print('set mega_split in .env')
        sys.exit(1)
    old_soap_split = load_split('C13.lss')
    old_run = Run(bs=old_soap_split)
    print(old_run.layout_path)
    print(old_run.render())


if __name__ == '__main__':
    main()
