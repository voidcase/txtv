# txtv - A client for reading swedish text tv in the terminal

Text-tv is great! plaintext and to-the-point news with no bullshit.
Now you can read it without touching your mouse or your tv-remote :)

![screenshot](https://raw.githubusercontent.com/voidcase/txtv/master/svtxtv_screenshot.png)

## Usage

Running with no arguments will enter interactive mode.
From there you can run any of these commands:

	help | h | ? -- show this help text.
	quit | q | exit -- quit the program (duh)
	list | ls | l -- list all articles
	next | n | > -- show next available page.
	previous | prev | p | < -- show previous available page.
	<PAGE NUMBER> -- show the page at the specified number

You can also give any of these arguments as an argument to run un-interactively. Except for `next` and `previous`, because that would make no sense.

	txtv.py 100

	txtv.py ls

## Configuration

txtv.py will automatically generate a config file at `~/.config/txtv/config` with default values.
Right now the most interesting thing there is aliases which work both in CLI mode and interactive mode. You can also change what your interactive prompt looks like if you care about that.

## Links

Here is the trello for the development of txtv: https://trello.com/b/aBI0DpN3/svtxtv

Here is where it's scraping data from: https://www.svt.se/svttext/web/pages/100.html
