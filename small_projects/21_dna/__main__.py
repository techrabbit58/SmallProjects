import random
import sys
import time

from .helix import helix

nucleotides = dict(zip('AGCT', 'TCGA'))


def main() -> None:
    for line in helix():
        left = random.choice(list(nucleotides))
        right = nucleotides[left]
        print(line.format(left, right) if line.find('{') > -1 else line)
        try:
            time.sleep(1 / 16)
        except KeyboardInterrupt:
            sys.exit()


main()
