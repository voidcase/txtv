import bs4
import requests as rq
import colorama
from colorama import Fore, Back, Style
import sys


def err(txt):
    print(Fore.RED + txt + Fore.RESET, file=sys.stderr)
    sys.exit(1)


def get_page_number() -> int:
    if len(sys.argv) == 0:
        return 100
    try:
        num = int(sys.argv[1])
    except ValueError:
        err('txtv <PAGE>\nexample: txtv 130')
    if num < 0:
        err('don\'t be so negative.')
    return num


def get_page(num) -> list:
    res = rq.get(f'https://www.svt.se/svttext/web/pages/{num}.html')
    if res.status_code == 404:
        err(f'There is no page number {num}. Pretty sure they start at 100.')
    elif res.status_code != 200:
        err(f'When i tried to get the page i just got HTTP status code {res.status_code}.')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    root = soup.find('pre', class_='root')
    rows = root.find_all('span')
    return rows


def show_page(rows:list):
    for row in rows:
        if row.get_text() == ' ' or 'bgB' in row.attrs['class']:
            continue
        style = ''
        if 'DH' in row.attrs['class']:
            style = Fore.YELLOW + Style.BRIGHT
        elif 'Y' in row.attrs['class']:
            style = Style.DIM
        print(style + row.get_text() + Style.RESET_ALL)

if __name__ == '__main__':
    colorama.init()
    page_nbr = get_page_number()
    rows = get_page(page_nbr)
    show_page(rows)
    colorama.deinit()
