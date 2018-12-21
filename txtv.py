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


def get_page(num) -> list:
    res = rq.get(f'https://www.svt.se/svttext/web/pages/{num}.html')
    if res.status_code != 200:
        err(f'When i tried to get the page i just got HTTP status code {res.status_code}.')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    root = soup.find('pre', class_='root')
    rows = root.find_all('span')
    return rows


def _filter_indentation_spans(rows: list) -> list: 
    return [
            row for row in rows
            if not (row.get_text() == ' ' or 'bgB' in row.attrs['class'])
            ]

def _merge_partial_rows(rows: list) -> list:
    ret = []
    itr = iter(rows)
    while True:
        row = None
        try:
            row = next(itr)
            while len(row.get_text()) < LINEWIDTH:
                row.append(next(itr))
                print('DBG:', row)
        except StopIteration:
            break
        if row:
            ret.append(row)
    return ret


def show_page(rows:list):
    until_next_break = LINEWIDTH
    for row in rows:
        if row.get_text() == ' ' or 'bgB' in row.attrs['class']:
            continue
        style = ''
        if 'DH' in row.attrs['class']:
            style = Fore.YELLOW + Style.BRIGHT
        elif 'Y' in row.attrs['class']:
            style = Style.DIM
        until_next_break -= len(row.get_text())
        print(style + row.get_text() + Style.RESET_ALL, end=('\n' if until_next_break <= 0 else ''))
        if until_next_break <= 0:
            until_next_break = LINEWIDTH

if __name__ == '__main__':
    colorama.init()
    page_nbr = get_page_number()
    rows = get_page(page_nbr)
    show_page(rows)
    colorama.deinit()
