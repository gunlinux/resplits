import os
import sys

from dotenv import load_dotenv
from ls import load_split

load_dotenv()


def main():
    mega_split_path = os.environ.get('mega_split')
    if not mega_split_path:
        print(':X')
        sys.exit(1)
    soap_split = load_split(mega_split_path)
    print(soap_split)


if __name__ == '__main__':
    main()
