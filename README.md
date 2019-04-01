# txtv - A client for reading swedish text tv in the terminal

Text-tv is great! plaintext and to-the-point news with no bullshit.
Now you can read it without touching your mouse or your tv-remote :)

![screenshot](https://raw.githubusercontent.com/voidcase/txtv/master/screenshot.png)

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

## Varför är inte denna texten på svenska, din ynkrygg?

Jag funderade på att skriva om readme och all text i programmet till svenska, eftersom man inte har så mycket nytta av det om man inte kan svenska ändå. Den huvudsakliga anledningen är att jag skrev det först på engelska av ren vana och har bara inte fått tummen ur nog att ändra det. Gör gärna en pull request om du känner att det är viktigt :)

du kan fortfarande köra med svenska kommandon om du lägger detta i din config fil:

	[alias]
		hjälp = help
		ut = quit
		lista = list
		nästa = next
		förra = prev

eller på skånska

	[alias]
		HjilpMaj = help
		LäggAuv = quit
		RaddaOpEt = list
		Nista = next
		NäeGåTebauka = prev

## Links

Here is the trello for the development of txtv: https://trello.com/b/aBI0DpN3/txtv

Here is where it's scraping data from: https://www.svt.se/svttext/web/pages/100.html
