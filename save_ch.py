import os
import sys

from dotenv import load_dotenv
from ls import load_split
from models import Run, get_chapter

load_dotenv()


def main():
    mega_split_path = os.environ.get('mega_split')
    if not mega_split_path:
        print('set mega_split in .env')
        sys.exit(1)
    old_soap_split = load_split(mega_split_path)
    old_run = Run(bs=old_soap_split)
    for level in old_run.levels:
        get_chapter(old_run, level)


if __name__ == '__main__':
    main()
