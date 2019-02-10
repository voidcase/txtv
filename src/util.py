from colorama import Fore, Back, Style
import sys

def err(txt: str, fatal=True):
    """Prints a red error message and quits with exit code 1."""
    print(Fore.RED + txt + Fore.RESET, file=sys.stderr)
    if fatal:
        sys.exit(1)
