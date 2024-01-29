import os
from dotenv import load_dotenv
from models import render_tpl
from get_diff import wrs


load_dotenv()
levels_path = 'lvls'
layout_path = 'layouts'

TPL_DIR = 'tpls'


def save_layout(name, text1, text2):
    tpl = render_tpl('layout.tpl', text1=text1, text2=text2)
    path = os.path.join(layout_path, f'{name}.lsl')
    print(f'saving to file {path}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(tpl)


def main():
    for key, value in wrs.items():
        save_layout(key, text1='wr', text2=value)


if __name__ == '__main__':
    main()
