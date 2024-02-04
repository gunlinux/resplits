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
