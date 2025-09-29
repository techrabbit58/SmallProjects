try:
    import pyperclip
except ModuleNotFoundError:
    print('Module "pyperclip" not found: clipboard feature not available.')


def rotate(ch: str, distance: int) -> str:
    candidates = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if ch not in candidates:
        return ch
    offset = (candidates.find(ch.lower()) + distance) % 26
    return candidates[offset] if ch.islower() else candidates[26 + offset]


def rot13(text: str) -> str:
    rotated = []
    for ch in text:
        rotated.append(rotate(ch, 13))
    return ''.join(rotated)


def copy_to_clipboard(text: str) -> bool:
    try:
        pyperclip.copy(text)
        return True
    except NameError:
        return False


def main(prog: str) -> None:
    while True:
        try:
            print(f'{prog}: Enter a message to encrypt or decrypt. Press <Ctrl-C> to quit.')
            response = input('> ').strip()
            if response == '':
                continue
            rotated = rot13(response)
            print(f'The translated message is:\n{rotated}\n')
            if copy_to_clipboard(rotated):
                print('(Copied to clipboard.)')
        except KeyboardInterrupt:
            break

    print('\nBye!')


if __name__ == '__main__':
    main('ROT13')
