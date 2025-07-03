from importlib import resources
from functools import partial

open_local_text_file = partial(resources.open_text, __package__)


def main() -> None:
    with open_local_text_file("foo.txt") as fd:
        print(fd.read())


main()
