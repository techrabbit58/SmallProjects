import caesarcode as caesar
import pyperclip

from .parser import get_argument_parser


def main():
    args = get_argument_parser('caesarcode').parse_args()
    text = ' '.join(args.message)
    match args.operation:
        case 'rot13':
            text = caesar.rot13(''.join(text))
        case 'encrypt':
            text = caesar.encrypt(args.key, text)
        case 'decrypt':
            text = caesar.decrypt(args.key, text)
    print(f'"{text}"')
    if args.clip:
        pyperclip.copy(text)
        print('Resulting text was copied to the clipboard.')


main()
