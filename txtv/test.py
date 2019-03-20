from pytest import fixture


def test_help(capsys):
    from txtv.txtv import cmd_help, commands
    cmd_help()
    cap = capsys.readouterr()
    assert len(cap.out.splitlines()) == 1 + len([c for c in commands if 'help' in c]) # header + commands
    assert len(cap.err) == 0


def test_list(capsys):
    import re
    from txtv.txtv import cmd_list, Page
    from colorama import Fore
    cmd_list()
    cap = capsys.readouterr()
    assert len(cap.err) == 0
    lines = cap.out.splitlines()
    for line in lines:
        assert len(line) == len(lines[0])
        num = int(line[-len(Fore.RESET)-3:-len(Fore.RESET)])
        Page(num)


# def test_next(capsys):
#     pass


# def test_prev(capsys):
#     pass


# def test_goto(capsys):
#     pass
