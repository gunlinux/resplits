import os

from jinja2 import Template
import sys

from dotenv import load_dotenv
from ls import load_split
from models import Run

load_dotenv()
levels_path = 'lvls'
layout_path = 'layouts'

TPL_DIR = 'tpls'
from  models import render_tpl
from get_diff import wrs


def  save_layout(name, text1, text2):
    tpl = render_tpl('layout.tpl', text1=text1, text2=text2)
    path = os.path.join(layout_path, f'{name}.lsl')
    print(f'saving to file {path}')
    with open(path, 'w') as f:
        f.write(tpl)


def main():
    for key, value  in wrs.items():
        save_layout(key, text1='wr', text2=value)

    
if __name__ == '__main__':
    main()
