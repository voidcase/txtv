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
        if 'Y' in row.attrs['class']:
            print(Fore.YELLOW + row.get_text() + Fore.RESET)
        else:
            print(row.get_text())
    colorama.deinit()
