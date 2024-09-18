import os.path
import sys
from pathlib import Path
import configparser


def main() -> None:
    cfg = configparser.ConfigParser()
    cfg.read(Path(os.path.dirname(sys.argv[0])) / 'magic_fortune_ball.conf')
    print(cfg.get('DEFAULT', 'replies').strip().split('\n'))


main()
