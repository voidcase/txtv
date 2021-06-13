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

cfg = get_config()

class Page:
    def __init__(self, num: int):
        self.num = num
        url = f'https://www.svt.se/svttext/web/pages/{num}.html'
        try:
            res = rq.get(url)
            if res.status_code != 200:
                err(f'Got HTTP status code {res.status_code}.')
            soup = bs4.BeautifulSoup(res.content, 'html.parser')
            self.subpages = soup.find_all('div', class_='Content_screenreaderOnly__Gwyfj')
        except rq.exceptions.RequestException:
            err(f"Could not get '{url}'.")

    def show(self, subpages=None) -> str:
        """Prints the page contained by the specified tag in color."""
        out = ''
        for page in subpages or self.subpages:
            pagetext: str = page.get_text()
            pagetext = pagetext.replace('\t', '')
            lines = pagetext.splitlines()
            filtered = ''
            for idx, line in enumerate(lines):
                if idx == 0 and not cfg.getboolean('show', 'svt_header'):
                    pass
                elif idx == 1 \
                        and 'PUBLICERAD' in line \
                        and not cfg.getboolean('show', 'publicerad_header'):
                    pass
                elif idx == len(lines) - 1 \
                        and re.match(r'.* [0-9]{3} +.* [0-9]{3} +.* [0-9]{3}', line) \
                        and not cfg.getboolean('show', 'navigation_footer'):
                    pass
                else:
                    filtered += line.rstrip() + '\n'
            out += filtered
        out = out.strip()
        return out

    def next_page(self):
        return Page(self.num + 1)

    def prev_page(self):
        return Page(self.num - 1)

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


def match_command(arg: str, interactive: bool=False) -> tuple:
    for cmd in commands:
        if interactive or 'interactive_only' not in cmd or not cmd['interactive_only']:
            match = re.fullmatch(str(cmd['pattern']), arg)
            if match:
                return cmd, match
    return None, None


def interactive(start_page: Page):
    print(start_page.show())
    state = dict(page=start_page)
    while True:
        try:
            print()
            prompt = cfg.get('general', 'prompt')
            raw = input(prompt + ' ').strip().lower()
            if cfg:
                raw = apply_aliases(raw, cfg)
            if raw == '':
                continue
            cmd, _ = match_command(raw, interactive=True)
            if cmd:
                print(cmd['func'](state=state, arg=raw), end='')
            else:
                err("That's not a command, kompis. 'help' gives you a list of commands.", fatal=False)
        except (EOFError, KeyboardInterrupt):
            print()
            exit(0)

 #####################
 # COMMAND FUNCTIONS #
 #####################

def cmd_help(**kwargs) -> str:
    def helpname(cmd: dict):
        '''Returns the name to show in the help text.'''
        if 'helpname' in cmd:
            return cmd['helpname']
        else:
            return re.sub(r'\|', r' | ', cmd['pattern'])

    out = Style.BRIGHT + Fore.YELLOW + 'Commands:' + Style.RESET_ALL + '\n'
    for cmd in commands:
        if 'help' in cmd:
            name = helpname(cmd)
            out += ('{}{} {}-- {}{}{}\n'.format(
                name,
                ' '*(max(len(helpname(cmd)) for cmd in commands) - len(name)),
                Style.DIM,
                cmd['help'],
                ' (only in interactive mode)'
                    if 'interactive_only' in cmd and cmd['interactive_only'] else '',
                Style.RESET_ALL
                ))
    return out


def cmd_next(state: dict, **kwargs) -> str:
    state['page'] = state['page'].next_page()
    return state['page'].show()


def cmd_prev(state: dict, **kwargs) -> str:
    state['page'] = state['page'].prev_page()
    return state['page'].show()


def cmd_list(**kwargs) -> str:
    from txtv.listing import list_all_articles
    out = ''
    articles = list_all_articles()
    for art in articles:
        if art:
            title, page_nbr = art
            out += title.ljust(37, '.') + Fore.BLUE + str(page_nbr) + Fore.RESET + '\n'
    return out


def cmd_page(arg: str, state: dict=None, **kwargs) -> str:
    try:
        num = validate_page_nbr(arg)
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
    if len(sys.argv) > 2:
        err('one arg only plz')
    if len(sys.argv) == 1:
        interactive(Page(100))
    else:
        raw_arg = sys.argv[1]
        real_arg = apply_aliases(raw_arg, cfg)
        cmd, _ = match_command(real_arg)
        if cmd:
            print(cmd['func'](arg=real_arg), end='')
            sys.exit(0)
        else:
            err("That's not a command, kompis. 'txtv help' gives you a list of commands.")
    colorama.deinit()

if __name__ == '__main__':
    run()

