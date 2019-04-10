import bs4
import requests as rq
import sys
import re
import colorama
import readline
from colorama import Fore, Back, Style
from pathlib import Path
from txtv.util import err
from txtv.config import get_config, apply_aliases, configparser


class Page:
    def __init__(self, num: int):
        self.num = num
        url = f'https://www.svt.se/svttext/web/pages/{num}.html'
        try:
            res = rq.get(url)
            if res.status_code != 200:
                err(f'Got HTTP status code {res.status_code}.')
            soup = bs4.BeautifulSoup(res.content, 'html.parser')
            self.subpages = soup.find_all('pre', class_='root')
            pn_links = soup.find('form', id='navform').find_all('a')
            self.prev, self.next = tuple(int(a.attrs['href'][:3]) for a in pn_links)
        except rq.exceptions.RequestException as e:
            err(f"Could not get '{url}'.")

    def show(self, subpages=None):
        """Prints the page contained by the specified tag in color."""
        out = ""
        for page in subpages or self.subpages:
            for node in page:
                if isinstance(node, str):
                    out += str(node)
                    continue
                style = ''
                if 'DH' in node.attrs['class']:
                    style = Fore.YELLOW + Style.BRIGHT
                elif 'Y' in node.attrs['class']:
                    style = Style.DIM
                elif 'bgB' in node.attrs['class']:
                    style = Fore.BLUE
                out += str(style + node.get_text() + Style.RESET_ALL)
        return out

    def next_page(self):
        return Page(self.next)

    def prev_page(self):
        return Page(self.prev)


def validate_page_nbr(arg: str) -> int:
    """
    Validates a page number, returns as int. Raises ValueError if bad.
    """
    try:
        num = int(arg)
    except ValueError:
        raise ValueError('txtv <PAGE>\nexample: txtv 130')
    if num < 100 or num > 999:
        raise ValueError('Text tv pages range from 100 to 999')
    return num


def match_command(arg: str, interactive=False):
    for cmd in commands:
        if interactive or 'interactive_only' not in cmd or not cmd['interactive_only']:
            m = re.fullmatch(cmd['pattern'], arg)
            if m:
                return cmd, m
    return None, None


def interactive(start_page: Page, cfg):
    print(start_page.show())
    state = dict(page=start_page)
    while True:
        try:
            prompt = cfg.get('general', 'prompt')
            raw = input(prompt or '> ').strip().lower()
            if cfg:
                raw = apply_aliases(raw, cfg)
            if raw == '':
                continue
            cmd, m = match_command(raw, interactive=True)
            if cmd:
                print(cmd['func'](state=state, match=m), end='')
            else:
                err("That's not a command, kompis. 'help' gives you a list of commands.", fatal=False)
        except (EOFError, KeyboardInterrupt):
            exit(0)


 #####################
 # COMMAND FUNCTIONS #
 #####################


def cmd_help(**kwargs):
    out = 'commands:\n'
    for cmd in commands:
        if 'help' in cmd:
            if 'helpname' in cmd:
                name = cmd['helpname']
            else:
                name = cmd['pattern']
                name = re.sub(r'\|', r' | ', name)
            out += ('{} -- {}{}\n'.format(
                name,
                cmd['help'],
                ' (only in interactive mode)'
                    if 'interactive_only' in cmd and cmd['interactive_only'] else ''
                ))
    return out


def cmd_next(state, **kwargs):
    state['page'] = state['page'].next_page()
    return state['page'].show()


def cmd_prev(state, **kwargs):
    state['page'] = state['page'].prev_page()
    return state['page'].show()


def cmd_list(**kwargs):
    from txtv.listing import list_all_articles
    out = ''
    articles = list_all_articles()
    for art in articles:
        if art:
            title, page_nbr = art
            out += title.ljust(36, '.') + Fore.BLUE + str(page_nbr) + Fore.RESET + '\n'
    return out


def cmd_page(match, state=None, cfg: configparser.ConfigParser=None, **kwargs):
    try:
        num = validate_page_nbr(match.group(0))
    except ValueError as e:
        err(str(e), fatal=(state is None))
        return ''
    if state:
        state['page'] = Page(num)
        return state['page'].show()
    else:
        return Page(num).show()


commands = [
    {
        'helpname':         'help | h | ?',
        'pattern':          r'h|\?|help',
        'func':             cmd_help,
        'help':             'show this help text.',
    },
    {
        'pattern':          'quit|q|exit',
        'func':             lambda **kwargs: sys.exit(0),
        'help':             'quit the program (duh)',
        'interactive_only': True,
    },
    {
        'pattern':          'list|ls|l',
        'func':             cmd_list,
        'help':             'list all articles',
    },
    {
        'pattern':          'next|n|>',
        'func':             cmd_next,
        'help':             'show next available page.',
        'interactive_only': True,
    },
    {
        'pattern':          'previous|prev|p|<',
        'func':             cmd_prev,
        'help':             'show previous available page.',
        'interactive_only': True,
    },
    {
        'helpname':         '<PAGE NUMBER>',
        'pattern':          '[0-9]+',
        'func':             cmd_page,
        'help':             'show the specified page',
    },
]


def run():
    colorama.init()
    cfg = get_config()
    if len(sys.argv) > 2:
        err('one arg only plz')
    if len(sys.argv) == 1:
        interactive(Page(100), cfg=cfg)
    else:
        raw_arg = sys.argv[1]
        real_arg = apply_aliases(raw_arg, cfg)
        cmd, m = match_command(real_arg)
        if cmd:
            print(cmd['func'](match=m, cfg=cfg), end='')
            sys.exit(0)
        else:
            err("That's not a command, kompis. 'txtv help' gives you a list of commands.")
    colorama.deinit()

if __name__ == '__main__':
    run()

