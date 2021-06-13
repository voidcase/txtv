# txtv - A client for reading swedish text tv in the terminal

Text-tv is great! plaintext and to-the-point news with no filler.
Now you can read it without touching your mouse or your tv-remote :)

## Installation

If you have Python 3.6 or later with pip installed, just run

	pip3 install --user txtv

Currently wont work natively on the Windows command line because of [readline](https://docs.python.org/3/library/readline.html); but you can use it with [Ubuntu for Windows](https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0).

## Usage

Running with no arguments will enter interactive mode.

	txtv

From there you can run any of these commands:

	help | h | ? -- show this help text.
	quit | q | exit -- quit the program (duh)
	list | ls | l -- list all articles
	next | n | > -- show next available page.
	previous | prev | p | < -- show previous available page.
	<PAGE NUMBER> -- show the page at the specified number

You can also give any of these commands as an argument on the normal command line to run un-interactively. Except for `quit`, `next`, and `previous`, because that would make no sense.

	txtv 100  # show page 100

	txtv ls   # list all news articles

## Configuration

txtv.py will automatically generate a config file at `~/.config/txtv/txtv.cfg` with default values. It uses format of [configparser](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure).

### alias

under the alias category you can specify any number of aliases for txtv commands. These will work both in interactive mode and as subcommands when calling txtv from your shell.

example:

	[alias]
		all=list

will let you list all articles from shell with

	txtv all

or by typing `all` in interactive mode.

### general

So far there is only one option here, named `prompt`. It is just the prompt string used in interactive mode.

example:

	[general]
		prompt = kommandorörelse>

## Links

Here is the trello for the development of txtv: https://trello.com/b/aBI0DpN3/txtv

Here is where it's scraping data from: https://www.svt.se/svttext/web/pages/100.html
