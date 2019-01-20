import bs4
import re
from txtv import get_page_loop, get_page
from pprint import pprint


def is_content_entry(tag: bs4.element.Tag):
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


def parse_content_listing(page: bs4.element.Tag) -> list:
    raw = ''
    for n in page.children:
        if isinstance(n, str):
            raw += n
            pass
        elif isinstance(n, bs4.element.Tag):
            if all((x not in n.attrs['class']) for x in ['bgB', 'bgY', 'Y']):
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


def test_content_listing():
    from pprint import pprint
    page = get_page(102)[0]
    content = parse_content_listing(page)
    pprint(content)
    assert False


def content_list() -> list:
    import re
    itempattern = r'(\w+)\.*(\d\d\d)'
    page = get_page(700)[0]
    spans = page.find_all('span')
    spans = [s for s in spans if len(list(s.children)) >= 2 and s.find('a')]
    return spans
    # return [re.findall(itempattern, node.get_text()) for node in page]


def list_all_articles():
    full_listing = []
    for nbr in [101, 104]:
        pages = get_page_loop(nbr, r'Fler rubriker ([0-9]{3})')
        for p in pages:
            full_listing += parse_content_listing(p)
    return full_listing
