from pytest import fixture

@fixture
def default_config():
    from txtv.config import CONFIG_DEFAULT_VALUES
    from configparser import ConfigParser
    return ConfigParser().read_dict(CONFIG_DEFAULT_VALUES)


def test_help():
    from txtv.txtv import cmd_help, commands
    out = cmd_help()
    assert len(out.splitlines()) == \
        1 + len([
            c for c in commands
            if 'help' in c
            ]) # header + commands


def test_list():
    import re
    from txtv.txtv import cmd_list, Page
    from colorama import Fore
    out = cmd_list()
    lines = out.splitlines()
    for line in lines:
        if len(line) == 0:
            continue
        assert len(line) == len(lines[0])
        num = int(line[-len(Fore.RESET)-3:-len(Fore.RESET)])
        Page(num)


def test_next():
    from txtv.txtv import Page, cmd_next
    state = dict(page=Page(100))
    out = cmd_next(state=state)
    assert state['page'].num == 101
    assert out.split()[0] == '101'


def test_prev():
    from txtv.txtv import Page, cmd_prev
    state = dict(page=Page(101))
    out = cmd_prev(state=state)
    assert state['page'].num == 100
    assert out.split()[0] == '100'


def test_page(default_config):
    from txtv.txtv import cmd_page
    out = cmd_page(arg='100', cfg=default_config)
    lines = out.splitlines()
    assert len(lines) == 21

