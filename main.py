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
    print(mega_split_path)
    old_soap_split = load_split(mega_split_path)
    old_run = Run(bs=old_soap_split)
    old_run.save_to_file('new_split.lss')
    new_soap_split = load_split('new_split.lss')
    new_run = Run(bs=new_soap_split)
    print(new_run.game_name)
    print(f'attemtpted counts {new_run.attempt_count}')
    print(f'segments count: {new_run.segments_count}')
    print(new_run.render())


if __name__ == '__main__':
    main()
