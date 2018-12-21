#!/usr/bin/env python3

import bs4
import requests as rq
import colorama
from colorama import Fore, Back, Style
import sys

LINEWIDTH = 38

def err(txt):
    print(Fore.RED + txt + Fore.RESET, file=sys.stderr)
    sys.exit(1)


def get_page_number() -> int:
    if len(sys.argv) > 2:
        err('Maybe we will support more arguments in the future, but not today.')
    if len(sys.argv) == 1:
        return 100
    try:
        num = int(sys.argv[1])
    except ValueError:
        err('txtv <PAGE>\nexample: txtv 130')
    if num < 100 or num > 999:
        err('Text tv pages range from 100 to 999')
    return num


def get_page(num: int) -> bs4.element.Tag:
    res = rq.get(f'https://www.svt.se/svttext/web/pages/{num}.html')
    if res.status_code != 200:
        err(f'When i tried to get the page i just got HTTP status code {res.status_code}.')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    subpages = soup.find_all('pre', class_='root')
    return subpages


def show_page(page: bs4.element.Tag):
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

if __name__ == '__main__':
    colorama.init()
    page_nbr = get_page_number()
    subpages = get_page(page_nbr)
    for page in subpages:
        show_page(page)
    colorama.deinit()
