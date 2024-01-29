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
            segment_bs = segment.bestsegmenttime
            bs = segment_bs.get_gametime()
            for main_segment in mega.segments:
                main_bs = main_segment.bestsegmenttime
                if main_segment.name == segment.name and main_bs.get_gametime() > bs:
                    print(f'{segment.name}  {main_bs.Gametime} > {segment_bs.Gametime}')
                    s += main_bs.get_gametime() - segment_bs.get_gametime()
                    main_bs.Gametime = segment_bs.Gametime
    print(f'improved  main run time by {Run.msecs_to_str(s)}')
    return mega


def update_runs(mega,  runs: list[Run]):
    print('Updating  single  lines')
    s = 0
    for run in runs:
        for segment in run.segments:
            segment_bs = segment.bestsegmenttime
            bs = segment_bs.get_gametime()
            for main_segment in mega.segments:
                main_bs = main_segment.bestsegmenttime
                if main_segment.name == segment.name and main_bs.get_gametime() < bs:
                    print(f'{segment.name}  {segment_bs.Gametime} > {main_bs.Gametime}')
                    s += segment_bs.get_gametime() - main_segment.bestsegmenttime.get_gametime()
                    segment_bs.Gametime = main_segment.bestsegmenttime.Gametime
                    run.updated = True
    print(f'improved  runs time by {Run.msecs_to_str(s)}')
    return runs


def main():
    mega_split_path = os.environ.get('mega_split')
    if not mega_split_path:
        print('set mega_split in .env')
        sys.exit(1)
    old_soap_split = load_split(mega_split_path)
    old_run = Run(bs=old_soap_split)
    old_run.save_to_file('new_split.lss')
    new_soap_split = load_split('new_split.lss')
    new_run = Run(bs=new_soap_split)
    print(new_run.levels)
    runs = load_levels(path=levels_path, levels=new_run.levels)
    mega = update_main(new_run, runs)
    mega.save_to_file(f'{os.environ.get("mega_split")}')
    runs = update_runs(mega, runs)
    for run in runs:
        if run.updated:
            run.layout_path = f'C:\\app\\projecs\\resplits\\layouts\\{run.name}.lsl'
            run.save_to_file(os.path.join(levels_path, f'{run.name}.lss'))


if __name__ == '__main__':
    main()
