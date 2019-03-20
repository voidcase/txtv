from pathlib import Path
import configparser

CONFIG_DIR = Path.home() / '.config' / 'txtv'
CONFIG_DEFAULT_PATH = CONFIG_DIR / 'txtv.cfg'

def get_or_gen_config(config_path: Path = CONFIG_DEFAULT_PATH):
    cfg = configparser.ConfigParser()
    if config_path.exists():
        cfg.read_file(open(config_path, 'r'))
    else:
        cfg['alias'] = {
                'inrikes':'101',
                'in':'101',
                'utrikes':'104',
                'ut':'104',
                'innehåll':'700',
                }
        cfg['general'] = {
                'prompt': 'txtv> ',
                }
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

