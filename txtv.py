import bs4
import requests as rq
import colorama
from colorama import Fore, Back, Style
from sys import argv


if __name__ == '__main__':
    colorama.init()
    page = int(argv[1])
    res = rq.get(f'https://www.svt.se/svttext/web/pages/{page}.html')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    root = soup.find('pre', class_='root')
    rows = root.find_all('span')
    for row in rows:
        if row.get_text() == ' ' or 'bgB' in row.attrs['class']:
            continue
        style = ''
        if 'DH' in row.attrs['class']:
            style = Fore.YELLOW + Style.BRIGHT
        elif 'Y' in row.attrs['class']:
            style = Style.DIM
        print(style + row.get_text() + Style.RESET_ALL)
    colorama.deinit()
