import bs4
import re
from txtv.txtv import Page
from pprint import pprint


def get_page_loop(start_num: int, pattern: str) -> list:
    pages = [Page(start_num)]
    while True:
        match = re.search(pattern, pages[-1].subpages[0].get_text())
        if not match or match.group(1) == str(start_num):
            break
        pages.append(Page(int(match.group(1))))
    return pages


def is_content_entry(tag: bs4.element.Tag) -> bool:
    # children = [
    #         c for c in tag.children
    #         if not (isinstance(c, str) and re.match(r' +', c))
    #         ]
    # children = list(tag.children)
    # return (
    #         tag.name == 'span'
    #         and 'W' in tag.attrs.['class']
    #         and len(children) >= 2
    #         and isinstance(children[-1], bs4.element.Tag)
    #         and all(isinstance(elem, str) for elem in children[:-1])
    #         and children[-1].name == 'a'
    #         )
    return (
            isinstance(tag, bs4.element.Tag)
            and tag.name == 'span'
            and all(not cls.startswith('bg') for cls in tag.attrs['class'])
            and any((c in tag.attrs['class']) for c in ['W', 'C'])
            and not re.fullmatch(' *', tag.get_text())
            )


def parse_content_listing(page: Page) -> list:
    raw = ''
    for n in page.subpages[0].children:
        if isinstance(n, str):
            raw += n
            pass
        elif isinstance(n, bs4.element.Tag):
            if 'class' not in n.attrs or all((x not in n.attrs['class']) for x in ['bgB', 'bgY', 'Y']):
                raw += n.get_text()
    entries = raw.splitlines()
    entries = [e for e in entries if not re.fullmatch(' *', e)]
    entries = [parse_content_entry(e) for e in entries]
    return entries


def parse_content_entry(line: str) -> tuple:
    m = re.fullmatch(r'(\* )?(.+[^.]).*[^0-9]([0-9]{3})[-f]?', line)

    if m:
        return (m.group(2).strip(), m.group(3))
    else:
        # raise RuntimeError(f'LINE DIDNT MATCH! {line}')
        return None


def list_all_articles() -> list:
    full_listing = []
    for nbr in [101, 104]:
        pages = get_page_loop(nbr, r'Fler rubriker ([0-9]{3})')
        for p in pages:
            full_listing += parse_content_listing(p)
    return full_listing

