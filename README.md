# txtv - A client for reading swedish text tv in the terminal

Text-tv is great! plaintext and to-the-point news with no bullshit.
Now you can read it without touching your mouse or your tv-remote :)

![screenshot](https://raw.githubusercontent.com/voidcase/txtv/master/txtv_screenshot.png)

## Installation

	pip install --user txtv

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

txtv.py will automatically generate a config file at `~/.config/txtv/txtv.cfg` with default values.
Right now the most interesting thing there is aliases which work both in CLI mode and interactive mode. You can also change what your interactive prompt looks like if you care about that.

## Links

Here is the trello for the development of txtv: https://trello.com/b/aBI0DpN3/txtv

Here is where it's scraping data from: https://www.svt.se/svttext/web/pages/100.html
