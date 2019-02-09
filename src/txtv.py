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
import argparse


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

    def next_page(self):
        return Page(self.next)

    def prev_page(self):
        return Page(self.prev)


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


def get_page_loop(start_num: int, pattern):
    pages = [get_page(start_num)[0]]
    while True:
        match = re.search(pattern, pages[-1].get_text())
        if not match or match.group(1) == str(start_num):
            break
        pages.append(get_page(int(match.group(1)))[0])
    return pages


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


def match_command(arg: str, interactive=False):
    for cmd in commands:
        if interactive or 'interactive_only' not in cmd or not cmd['interactive_only']:
            m = re.fullmatch(cmd['pattern'], arg)
            if m:
                return cmd, m
    return None, None


def interactive(start_page: Page):
    start_page.show()
    state = dict(page=start_page)
    while True:
        try:
            raw = input('> ').strip().lower()
            cmd, m = match_command(raw, interactive=True)
            cmd['func'](state=state, match=m)
        except EOFError:
            exit(0)

    # while running:
    #     try:
    #         cmd = input('> ').strip().lower()
    #         if cmd == '':
    #             pass
    #         elif cmd == 'help':
    #             print('here will be a helptext later') # TODO
    #         elif cmd in ['quit', 'q', 'exit']:
    #             running = False
    #         elif cmd in ['next', 'n', 'j', '>']:
    #             page = Page(page.next)
    #             page.show()
    #         elif cmd in ['previous', 'prev', 'p', 'k', '<']:
    #             page = Page(page.prev)
    #             page.show()
    #         elif re.fullmatch('[1-9][0-9][0-9]',cmd):
    #             nbr = int(cmd)
    #             page = Page(int(cmd))
    #             page.show()
    #         else:
    #             print("That's not a command, type help for help, or quit to quit.")
    #     except EOFError:
    #         running = False


#####################
# COMMAND FUNCTIONS #
#####################

def cmd_help(**kwargs):
    print('commands:')
    for cmd in commands:
        if 'help' in cmd:
            if 'helpname' in cmd:
                name = cmd['helpname']
            else:
                name = cmd['pattern']
                name = re.sub('\|', ' | ', name)
            print('{} -- {}'.format(name, cmd['help']))


def cmd_next(state, **kwargs):
    state['page'] = state['page'].next_page()
    state['page'].show()


def cmd_prev(state, **kwargs):
    state['page'] = state['page'].prev_page()
    state['page'].show()


def cmd_list(**kwargs):
    from listing import list_all_articles
    articles = list_all_articles()
    for art in articles:
        if art:
            title, page_nbr = art
            print(title.ljust(38, '.'), Fore.BLUE + str(page_nbr) + Fore.RESET)


def cmd_page(match, state=None, **kwargs):
    num = validate_page_nbr(match.group(0))
    if state:
        state['page'] = Page(num)
        state['page'].show()
    else:
        Page(num).show()


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

commands = [
    {
        'pattern' : 'h|\?|help',
        'func': cmd_help,
        'help':'show this help text.',
    },
    {
        'pattern' : 'q|quit|exit',
        'func': lambda **kwargs: sys.exit(0),
        'help':'quit the program (duh)',
        'interactive_only' : True,
    },
    {
        'pattern' : 'l|ls|list',
        'func': cmd_list,
        'help':'list all articles',
    },
    {
        'pattern':'n|next|>',
        'func': cmd_next,
        'interactive_only' : True,
    },
    {
        'pattern':'previous|prev|p|<',
        'func': cmd_prev,
        'interactive_only' : True,
    },
    {
        'helpname' : '<PAGE NUMBER>',
        'pattern':'[0-9]{3}',
        'func': cmd_page,
        'help':'show the specified page',
    },
]


if __name__ == '__main__':
    colorama.init()
    cfg = get_or_gen_config()
    if len(sys.argv) > 2:
        err('one arg only plz')
    if len(sys.argv) == 1:
        interactive(Page(100))
    else:
        raw_arg = sys.argv[1]
        real_arg = apply_aliases(raw_arg, cfg)
        cmd, m = match_command(real_arg)
        if cmd:
            cmd['func'](match=m, cfg=cfg)
            sys.exit(0)
        else:
            err("That's not a command, kompis. 'help' gives you a list of commands.")
    colorama.deinit()
