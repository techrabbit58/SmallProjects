import shutil
import textwrap
from dataclasses import dataclass, field

UP_DOWN = '\u2503'
LEFT_RIGHT = '\u2501'
DOWN_RIGHT = '\u250f'
DOWN_LEFT = '\u2513'
UP_RIGHT = '\u2517'
UP_LEFT = '\u251B'
UP_DOWN_RIGHT = '\u2523'
UP_DOWN_LEFT = '\u252B'
DOWN_LEFT_RIGHT = '\u2533'
UP_LEFT_RIGHT = '\u253b'
CROSS = '\u254B'
CURSOR = '#'
SKIP = ' '


def get_command() -> str:
    print(textwrap.dedent("""
    Get a command: a sequence of WASD to move the pen, H for help, C to clear, F to save, or (Q)uit.
    """).strip())
    return input('> ').upper()


def get_help():
    return textwrap.dedent("""
    Enter sequences of W, A, S and D to move the cursor and
    draw a line behind it as it moves.
    
    For example, 'ddd' draws a line going right and 'sssdddwwwaaa'
    draws a box.
    
    Drawings can be saved to a file by entering (F)ile.
    (C)lear wipes out the drawing.
    """).strip()


@dataclass
class Position:
    x: int
    y: int

    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def reset(self) -> None:
        self.x = self.y = 0


opposite_of = dict(zip('WSAD', 'SWDA'))


@dataclass
class Canvas:
    width: int = field(kw_only=True)
    height: int = field(kw_only=True)
    screen: dict[tuple[int, int], set[str]] = field(init=False, default_factory=dict)

    def update(self, command: str, pos: Position) -> Position:
        """
        update the direction set for this screen position.
        advance the cursor.
        :param command: the movement command that updates the current cell and advances the cursor
        :param pos: the current column 0 <= x < width and row 0 <= x <= height
        :return: the updated cursor position
        """
        if not self.screen:  # avoid index errors and handle position (0, 0) correctly
            if command in set('WS'):
                self.screen[pos.as_tuple()] = set('S')
            elif command in set('AD'):
                self.screen[pos.as_tuple()] = set('D')

        if command == 'W' and pos.y > 0:
            self.screen[pos.as_tuple()].add(command)
            pos.y -= 1
        elif command == 'S' and pos.y < self.height - 1:
            self.screen[pos.as_tuple()].add(command)
            pos.y += 1
        elif command == 'A' and pos.x > 0:
            self.screen[pos.as_tuple()].add(command)
            pos.x -= 1
        elif command == 'D' and pos.x < self.width - 1:
            self.screen[pos.as_tuple()].add(command)
            pos.x += 1

        if pos.as_tuple() not in self.screen:
            self.screen[pos.as_tuple()] = set()

        self.screen[pos.as_tuple()].add(opposite_of[command])

        return pos

    def reset(self) -> None:
        self.screen = {}

    def to_string(self, pos: Position = None) -> str:
        if pos is None:
            pos = Position(-1, -1)

        canvas_string = []

        def update_canvas_string(cell: set[str]):
            if row == pos.y and col == pos.x:
                canvas_string.append(CURSOR)
                return

            if cell in (set('WS'), set('W'), set('S')):
                canvas_string.append(UP_DOWN)
            elif cell in (set('AD'), set('A'), set('D')):
                canvas_string.append(LEFT_RIGHT)
            elif cell == set('SD'):
                canvas_string.append(DOWN_RIGHT)
            elif cell == set('AS'):
                canvas_string.append(DOWN_LEFT)
            elif cell == set('WD'):
                canvas_string.append(UP_RIGHT)
            elif cell == set('WA'):
                canvas_string.append(UP_LEFT)
            elif cell == set('WSD'):
                canvas_string.append(UP_DOWN_RIGHT)
            elif cell == set('WSA'):
                canvas_string.append(UP_DOWN_LEFT)
            elif cell == set('ASD'):
                canvas_string.append(DOWN_LEFT_RIGHT)
            elif cell == set('WAD'):
                canvas_string.append(UP_LEFT_RIGHT)
            elif cell == set('WASD'):
                canvas_string.append(CROSS)
            else:
                canvas_string.append(SKIP)

        for row in range(self.height):
            for col in range(self.width):
                update_canvas_string(self.screen.get((col, row)))

            canvas_string.append('\n')

        return ''.join(canvas_string)

    def save_to_file(self, moves: list[str]) -> tuple[str, str]:
        filename = None

        try:
            print('Enter a filename to save to:')
            filename = input('enter filename: ')
            if not filename.endswith('.txt'):
                filename += '.txt'
            with open(filename, 'x', encoding='utf8') as f:
                print(''.join(moves), file=f)
                print(self.to_string(), file=f)
        except Exception as ex:
            return filename, str(ex)

        return filename, 'OK'


def main(prog: str):
    width, height = shutil.get_terminal_size()

    canvas = Canvas(width=width - 1, height=height - 4)
    pos = Position(0, 0)

    moves = []

    message = False

    while True:
        if not message:
            print(prog, '...', f'(row={pos.y}, col={pos.x})')
        message = False

        print(canvas.to_string(pos))
        response = get_command()

        if not response:
            continue

        if response in {'H', 'HELP'}:
            print(get_help())
            continue

        if response in {'Q', 'QUIT'}:
            print('Bye!')
            return

        if response in {'C', 'CLEAR'}:
            canvas.reset()
            pos.reset()
            continue

        if response in {'F', 'FILE'}:
            filename, message = canvas.save_to_file(moves)
            if message == 'OK':
                print(f'Canvas has been saved to file "{filename}"')
            else:
                print(f'Error! Could not write file "{filename}": {message}')
            message = True
            continue

        for command in response:
            if command not in set('WASD'):
                continue

            moves.append(command)
            pos = canvas.update(command, pos)


if __name__ == '__main__':
    main('Etching Drawer')
