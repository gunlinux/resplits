import os
import sys

from dotenv import load_dotenv
from ls import load_split
from models import Run

load_dotenv()


def main():
    mega_split_path = os.environ.get('mega_split')
    if not mega_split_path:
        print('set mega_split in .env')
        sys.exit(1)
    soap_split = load_split(mega_split_path)
    run = Run(bs=soap_split)
    print(run.game_name)
    print(f'attemtpted counts {run.attempt_count}')
    print(f'segments count: {run.segments_count}')
    print(run.render())


if __name__ == '__main__':
    main()
