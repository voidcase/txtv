#!/usr/bin/env python3

import bs4
import requests as rq
import sys
import re
import configparser
import colorama
from colorama import Fore, Back, Style
from util import err
from pathlib import Path

CONFIG_DIR = Path.home() / '.config' / 'svtxtv'

def validate_page_nbr(arg: str) -> int:
    """
    Validates a page number, returns as int. Complains to user if bad.
    """
    try:
        num = int(arg)
    except ValueError:
        err('txtv <PAGE>\nexample: txtv 130')
    if num < 100 or num > 999:
        err('Text tv pages range from 100 to 999')
    return num


def get_page(num: int) -> list:
    """
    Returns a list of the tags containing
    the page and potential subpages (type: bs4.element.Tag)
    on the specified page number.
    For most pages this will be a list of one element.
    """
    res = rq.get(f'https://www.svt.se/svttext/web/pages/{num}.html')
    if res.status_code != 200:
        err(f'Got HTTP status code {res.status_code}.')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    subpages = soup.find_all('pre', class_='root')
    return subpages


def get_page_loop(start_num: int, pattern):
    pages = [get_page(start_num)[0]]
    while True:
        match = re.search(pattern, pages[-1].get_text())
        if not match or match.group(1) == str(start_num):
            break
        pages.append(get_page(int(match.group(1)))[0])
    return pages

def test_page_loop():
    pages = get_page_loop(101)
    print(f'number of pages = {len(pages)}')
    for p in pages:
        print(p.get_text())
    assert False


def show_page(page: bs4.element.Tag):
    # def nodetext(node, parent_style=''):
    #     if isinstance(node, str):
    #         return node
    #     elif isinstance(node, bs4.element.Tag):
    #         if node.name == 'a':
    #             return Fore.RED + node.get_text() + Fore.RESET + parent_style
    #         else:
    #             return ''.join([nodetext(child) for child in node.children])
    """Prints the page contained by the specified tag in color.""" 
    for node in page:
        if isinstance(node, str):
            print(node, end='')
            continue
        style = ''
        if 'DH' in node.attrs['class']:
            style = Fore.YELLOW + Style.BRIGHT
        elif 'Y' in node.attrs['class']:
            style = Style.DIM
        elif 'bgB' in node.attrs['class']:
            style = Fore.BLUE
        print(style + node.get_text() + Style.RESET_ALL, end='')

def show_headers():
    from listing import list_all_articles
    articles = list_all_articles()
    for title, page_nbr in articles:
        print(title.ljust(38, '.'), Fore.BLUE + str(page_nbr) + Fore.RESET)


def get_or_gen_config(config_path=CONFIG_DIR / 'svtxtv.conf'):
    cfg = configparser.ConfigParser()
    if config_path.exists():
        cfg.read_file(open(config_path, 'r'))
    else:
        cfg['color'] = {
                'header' : 'yellow',
                'frame' : 'blue',
                }
        cfg['alias'] = {
                '__DEFAULT__' : '100',  # magic alias, will be used when given no arguments.
                'inrikes':'101',
                'in':'101',
                'utrikes':'104',
                'ut':'104',
                'innehåll':'700',
                }
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir()
        cfg.write(open(config_path, 'w'))
    return cfg


def apply_aliases(txt: str, cfg: configparser.ConfigParser) -> str:
    txt = txt.strip()
    if 'alias' in cfg and txt in cfg['alias']:
        return cfg['alias'][txt]
    else:
        return txt


if __name__ == '__main__':
    colorama.init()
    cfg = get_or_gen_config()
    raw_arg = '__DEFAULT__'
    if len(sys.argv) > 2:
        err('one arg only plz')
    if len(sys.argv) == 2:
        raw_arg = sys.argv[1]
    real_arg = apply_aliases(raw_arg, cfg)
    if real_arg == 'head':
        show_headers()
    else:
        page_nbr = validate_page_nbr(real_arg)
        try:
            subpages = get_page(page_nbr)
        except rq.exceptions.ConnectionError:
            err('Could not connect to network :(')
        for page in subpages:
            show_page(page)
    colorama.deinit()
