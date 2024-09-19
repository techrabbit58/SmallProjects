import os.path
import random
import sys
from pathlib import Path
import configparser


def main() -> None:
    cfg = configparser.ConfigParser()
    cfg.read(Path(os.path.dirname(sys.argv[0])) / 'magic_fortune_ball.ini')
    print(random.choice(cfg.get('DEFAULT', 'replies').strip().split('\n')))
    print(random.choice(cfg.get('DEFAULT', 'answers').strip().split('\n')))


main()
