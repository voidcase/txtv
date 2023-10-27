import requests as rq
import sys
import re
import regex
import colorama
import readline
import json
import textwrap
from colorama import Fore, Back, Style
from pathlib import Path
from txtv.util import err
from txtv.config import get_config, apply_aliases, configparser

cfg = get_config()

class Page:
    def __init__(self, num: int):
        self.num = num
        self.contententries = []
        url = f'https://api.teletext.ch/channels/SRF1/pages/{num}'
        self.haspages = True
        # Either a news page (first format) or a TV page (second)
        self.dateformat = r'(\s{2,}\d{2}\.\d{2}\.\d{2}\s\d{2}:\d{2})|(\d{2}.*\d{2}:\d{2}-\d{2}:\d{2})'
        self.titleformat = r'(.*?\d{2}\.\d{2}\.\d{2}\s\d{2}:\d{2})|(.*\d{2}:\d{2}-\d{2}:\d{2})'


        try:
            res = rq.get(url)
            if res.status_code != 200:
                err(f'Got HTTP status code {res.status_code}.')
            page = json.loads(res.content)
            self.content = page["subpages"][0]["ep1Info"]["contentText"]

            # Leaf pages have the date on top
            self.haspages = not re.search(self.dateformat, self.content)

            if not self.has_pages():
                # Extract and remove title from content
                split = re.split(self.titleformat, self.content)
                split = list(filter(None, split))
                self.title = split[0]
                self.content = split[1]
                return

            # Keep the uppercase titles
            stories = self.content

            if self.num == 100 or self.num == 700:
                # Remove actual titles
                stories = re.sub("Jetzt auf SRF 1", "", stories)
                stories = re.sub("JETZT AUF SRF 1", "", stories)
                stories = re.sub("TELETEXT SRF 1", "", stories)
            else:
                # Remove all uppercase subtitles. There can be multiple
                # subtitles on a page (subtitle, stories, subtitle, stories, etc)
                stories = regex.sub(r'[\p{Lu}\s-]{9,}[\s:]', '', self.content)

            # Find all three digit numbers, most probably these are page numbers
            page_nrs = re.findall(r'\s(\d{3})*[-\/]*(\d{3})([^\d]|$)', stories)
            all_page_nrs = []

            for p in page_nrs:
                try:
                    n = int(p[0])
                    all_page_nrs.append(n)
                except:
                    pass
                try:
                    n = int(p[1])
                    all_page_nrs.append(n)
                except:
                    pass

            all_page_nrs = [str(p) for p in all_page_nrs]

            entries = []
            i = 0
            entry = ""

            # Split content by whitespaces
            chunks = stories.split()

            # Include all chunks on overview/tv pages
            if self.num != 100 and self.num != 700:
                # Discard the title chunks (headings)
                chunks = chunks[4:]
                #all_page_nrs = all_page_nrs[2:]

            for chunk in chunks:
                if i+1 >= len(all_page_nrs):
                    # Add all remaining text from that page to last chunk
                    entry += chunk + " "
                    continue

                # Add the chunk to the current entry
                entry += chunk + " "

                # If the chunk is indeed in the list of next potential page numbers
                if all_page_nrs[i] in chunk or chunk in all_page_nrs[i:]:
                    # Check for ascending page numbers
                    #if int(page_nrs[i+1]) > int(chunk):
                    # Add the entry to the list of all entries
                    entries.append(entry.strip())
                    entry = ""
                    #else:
                    i += 1

            # Add last entry with remaining text
            entries.append(entry.strip())
            self.contententries = entries

        except rq.exceptions.RequestException:
            err(f"Could not get '{url}'.")

    def has_pages(self) -> bool:
        if self.num in [100, 104, 180, 130, 500, 150, 700]:
            return True
        else:
            return self.haspages

    def show(self) -> str:
        """Prints the page contained by the specified tag in color."""
        out = ''

        if not self.has_pages():
            out = '\n' + Style.BRIGHT + textwrap.fill(self.title.strip(), 37) + '\n\n' + Style.RESET_ALL
            out += textwrap.fill(self.content.strip(), 37)
            return out

        articles = []
        append = ""
        for e in self.contententries:
            parsed_entry = parse_content_entry(append + e)
            if parsed_entry == None:
                # No clear page number found, assume this belongs to next entry
                append += e
            else:
                articles += [parsed_entry]
                append = ''

        #prev_nr = int(articles[0][1])-1
        for art in articles:
            if art:
                title, page_nbr = art
                # if int(prev_nr)+1 != int(page_nbr):
                #     print("wrong article order")
                #prev_nr = page_nbr
                out += title.ljust(37, '.') + Fore.BLUE + str(page_nbr) + Fore.RESET + '\n'

        return out

    def next_page(self):
        return Page(self.num + 1)

    def prev_page(self):
        return Page(self.num - 1)

def list_all_articles() -> list:
    full_listing = []
    for nbr in [104, 130]:
        page = Page(nbr)
        if not page.has_pages():
            continue
        full_listing += [parse_content_entry(e) for e in page.contententries]
    return full_listing

def parse_content_entry(line: str) -> tuple:
    m = re.fullmatch(r'(.*)\s(\d{3}[-\/]*).*', line)

    if m:
        return (m.group(1).strip(), m.group(2))
    else:
        # raise RuntimeError(f'LINE DIDNT MATCH! {line}')
        return None

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
