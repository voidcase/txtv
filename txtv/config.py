from pathlib import Path
import configparser

CONFIG_DIR = Path.home() / '.config' / 'txtv'
CONFIG_DEFAULT_PATH = CONFIG_DIR / 'txtv.cfg'
CONFIG_DEFAULT_VALUES = {
    'alias' : { },
    'general' : {
        'prompt': 'txtv>',
    },
    'show': {
        'svt_header': 'yes',
        'publicerad_header': 'yes',
        'navigation_footer': 'yes',
    },
}

def get_config(config_path: Path = CONFIG_DEFAULT_PATH) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read_dict(CONFIG_DEFAULT_VALUES)
    if config_path and config_path.exists():
        cfg.read_file(open(config_path, 'r'))
    else:
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir()
        cfg.write(open(config_path, 'w'))
    return cfg


def apply_aliases(txt: str, cfg: configparser.ConfigParser) -> str:
    txt = txt.strip()
    if 'alias' in cfg and txt in cfg['alias']:
        return cfg['alias'][txt]
    else:
        return txt
