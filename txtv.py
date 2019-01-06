#!/usr/bin/env python3

import bs4
import requests as rq
import colorama
from colorama import Fore, Back, Style
import sys
import re
from util import err


def get_page_number() -> int:
    """
    Parses and input validates the page number argument,
    returns it as an int.
    """
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


def show_page(page: bs4.element.Tag, parent_style=''):
    def nodetext(node):
        if isinstance(node, str):
            return node
        elif isinstance(node, bs4.element.Tag):
            if node.name == 'a':
                return Fore.RED + node.get_text() + Fore.RESET + parent_style
            else:
                return ''.join([nodetext(child) for child in node.children])
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
        print(style + nodetext(node) + Style.RESET_ALL, end='')

def show_headers():
    from listing import list_all_articles
    articles = list_all_articles()
    for title, page_nbr in articles:
        print(title.ljust(38, '.'), Fore.BLUE + str(page_nbr) + Fore.RESET)

if __name__ == '__main__':
    colorama.init()
    if len(sys.argv) == 2 and sys.argv[1] == 'head':
        show_headers()
    else:
        page_nbr = get_page_number()
        try:
            subpages = get_page(page_nbr)
        except rq.exceptions.ConnectionError:
            err('Could not connect to network :(')
        for page in subpages:
            show_page(page)
    colorama.deinit()
