import argparse

import caesarcode as caesar


def parsed_args(prog: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=prog, description='A brute force decoder for the trivial Caesar cypher')
    parser.add_argument('words', help='The message that shall be uncovered.', nargs='+')
    return parser.parse_args()


def main(prog: str):
    words = parsed_args(prog).words
    for key in caesar.ALPHABET:
        sentence = []
        for word in words:
            sentence.append(caesar.decrypt(key, word))
        print(f'{key=}: "{" ".join(sentence)}"')


if __name__ == '__main__':
    main('uncaesar')
