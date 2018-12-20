import bs4
import requests as rq
from sys import argv


if __name__ == '__main__':
    page = int(argv[1])
    res = rq.get(f'https://www.svt.se/svttext/web/pages/{page}.html')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    root = soup.find('pre', class_='root')
    rows = [ s.get_text() for s in root.find_all() if s.get_text() != ' ' ]
    for r in rows:
        print(r)
