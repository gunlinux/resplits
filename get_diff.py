import os
import sys

from dotenv import load_dotenv
from ls import load_split
from models import Run

load_dotenv()


wrs = {
    "C1": "00:0:40.960",
    "C2": "00:1:56.810",
    "C3": "00:2:22.080",
    "C4.1": "00:0:20.650",
    "C4.2": "00:1:33.530",
    "C5.1": "00:2:22.310",
    "C5.2": "00:2:56.270",
    "C6.1": "00:0:31.040",
    "C6.2": "00:0:33.880",
    "C7": "00:3:16.140",
    "C8": "00:1:54.040",
    "C9": "00:1:06.950",
    "C10": "00:2:17.120",
    "C11": "00:2:33.610",
    "C12": "00:2:32.020",
    "C13": "00:4:09.630",
    "C14": "00:3:54.150",
}


def get_comp(rez):
    wrs_with_msecs = {level: Run.get_msecs(value) for level, value in wrs.items()}
    diffs = {}
    for level, value in wrs_with_msecs.items():
        diffs[level] = value - rez[level]

    d = dict(sorted(diffs.items(), key=lambda item: item[1]))
    for item, value in d.items():
        d[item] = value/1_000_000
    for item, value in d.items():
        print(f'{item}: {value}')


def main():
    mega_split_path = os.environ.get('mega_split')
    if not mega_split_path:
        print('set mega_split in .env')
        sys.exit(1)
    old_soap_split = load_split(mega_split_path)
    run = Run(bs=old_soap_split)
    rez = run.get_levels_pb()
    golds = run.get_levels_golds()
    get_comp(rez)
    print()
    get_comp(golds)
    print(f'attemtpted counts {run.attempt_count}')
    print(f'segments count: {run.segments_count}')


if __name__ == '__main__':
    main()
