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

### show

Here you can filter out some parts of the pages you might find unnecessary or distracting. These are all boolean variables and the accepted values are those that [configparser accepts as true/false](https://docs.python.org/3/library/configparser.html#configparser.ConfigParser.BOOLEAN_STATES):

> ... config parsers consider the following values True: '1', 'yes', 'true', 'on' and the following values False: '0', 'no', 'false', 'off'.

these are all on by default.


| Option | Description |
| ------ | ----------- |
| svt_header | The line at the top that looks like `100 SVT Text         Fredag 12 apr 2019`. Keep in mind that turning this off might make it hard to keep track of what page you are on in interactive mode. HMU or make a PR if you would like to see only the page number.|
| publicerad_header | The blue line that says when the article was published (`INRIKES PUBLICERAD  12 APRIL`) |
| navigation_footer | The bottom line that usually says `Inrikes 101 Utrikes 104 Innehåll 700`. If it does not follow this format (like when the article continues on the next page) it will still be shown. |


Right now the most interesting thing there is aliases which work both in CLI mode and interactive mode. You can also change what your interactive prompt looks like if you care about that.


## Links

Here is the trello for the development of txtv: https://trello.com/b/aBI0DpN3/txtv

Here is where it's scraping data from: https://www.svt.se/svttext/web/pages/100.html
