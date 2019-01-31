#!/usr/bin/env python3

import bs4
import requests as rq
import sys
import re
import colorama
from colorama import Fore, Back, Style
from util import err
from pathlib import Path
from config import get_or_gen_config, apply_aliases

class Page:
    def __init__(self, num: int):
        self.num = num
        res = rq.get(f'https://www.svt.se/svttext/web/pages/{num}.html')
        if res.status_code != 200:
            err(f'Got HTTP status code {res.status_code}.')
        soup = bs4.BeautifulSoup(res.content, 'html.parser')
        self.subpages = soup.find_all('pre', class_='root')
        pn_links = soup.find('form', id='navform').find_all('a')
        self.prev, self.next = tuple(int(a.attrs['href'][:3]) for a in pn_links)

    def show(self, subpages=None):
        """Prints the page contained by the specified tag in color.""" 
        for page in subpages or self.subpages:
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

    def next():
        return Page(this.next)

    def prev():
        return Page(this.prev)


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
    for art in articles:
        if art:
            title, page_nbr = art
            print(title.ljust(38, '.'), Fore.BLUE + str(page_nbr) + Fore.RESET)

def interactive(start_page: Page):
    start_page.show()
    page = start_page
    running = True
    while running:
        try:
            cmd = input('> ')
            if cmd == '':
                pass
            elif cmd == 'help':
                print('here will be a helptext later') # TODO
            elif cmd in ['quit', 'q', 'exit']:
                running = False
            elif cmd.lower() in ['next', 'n', 'j', '>']:
                page = Page(page.next)
                page.show()
            elif cmd.lower() in ['previous', 'prev', 'p', 'k', '<']:
                page = Page(page.prev)
                page.show()
            else:
                print("That's not a command, type help for help, or quit to quit.")
        except EOFError:
            running = False


if __name__ == '__main__':
    IFLAG = True
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
            page = Page(page_nbr)
            if IFLAG:
                interactive(page)
            else:
                page.show()
        except rq.exceptions.ConnectionError:
            err('Could not connect to network :(')
    colorama.deinit()
