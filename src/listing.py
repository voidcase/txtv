import bs4
import re
from txtv import get_page_loop, get_page
from pprint import pprint


def is_content_entry(tag: bs4.element.Tag):
    # children = [
    #         c for c in tag.children
    #         if not (isinstance(c, str) and re.match(r' +', c))
    #         ]
    children = list(tag.children)
    return (
            tag.name == 'span'
            and len(children) >= 2
            and isinstance(children[-1], bs4.element.Tag)
            and all(isinstance(elem, str) for elem in children[:-1])
            and children[-1].name == 'a'
            )


def parse_content_entry(tag: bs4.element.Tag) -> tuple:
    # children = [
    #         c for c in tag.children
    #         if not (isinstance(c, str) and re.match(r' +', c))
    #         ]
    children = list(tag.children)
    if is_content_entry(tag):
        title = re.search(r'^(.+[^.])\.*$', ''.join(children[:-1])).group(1).strip()
        num = children[-1].get_text()
        return title, num
    else:
        return None, None


def parse_content_listing(page: bs4.element.Tag) -> list:
    return [
            parse_content_entry(span)
            for span in page.find_all('span')
            if is_content_entry(span)
            ]

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
