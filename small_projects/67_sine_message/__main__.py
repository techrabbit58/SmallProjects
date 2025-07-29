import argparse


def get_args(title: str) -> str:
    parser = argparse.ArgumentParser(prog=title)
    parser.add_argument(
        "message", nargs=argparse.ONE_OR_MORE,
        help="The message to display (max. 39 characters)"
    )
    message = parser.parse_args().message
    return " ".join(message)[:39]


def main(title: str) -> None:
    message = get_args(title)
    print(message)


if __name__ == '__main__':
    main("sinemessage")