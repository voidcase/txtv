from colorama import Fore, Back, Style
import sys

def err(txt: str):
    """Prints a red error message and quits with exit code 1."""
    print(Fore.RED + txt + Fore.RESET, file=sys.stderr)
    sys.exit(1)
