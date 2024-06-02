import argparse


class PrepareOpAndKey(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, {
            '-e': 'encrypt',
            '--encrypt': 'encrypt',
            '-d': 'decrypt',
            '--decrypt': 'decrypt',
            '--rot13': 'rot13'
        }.get(option_string))
        setattr(namespace, 'key', 'N' if option_string == '--rot13' else values.upper())


def get_argument_parser(prog: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog, description='Encrypt or decrypt a given message using the Caesar cypher.')

    group = parser.add_argument_group('encryption settings')
    ex_group = group.add_mutually_exclusive_group(required=True)

    ex_group.add_argument(
        '--rot13', help='perform rot13 style encoding and decoding',
        action=PrepareOpAndKey, nargs=0, dest='operation')
    ex_group.add_argument(
        '-e', '--encrypt', help='encrypt the given plain text using the given key',
        action=PrepareOpAndKey, dest='operation')
    ex_group.add_argument(
        '-d', '--decrypt', help='decrypt the given encrypted text using the given key',
        action=PrepareOpAndKey, dest='operation')

    parser.add_argument('-c', '--clip', help='copy the output to the clipboard', action='store_true')

    parser.add_argument(
        'message', help='the message text that shall be encrypted or decrypted',
        nargs='+')

    return parser
