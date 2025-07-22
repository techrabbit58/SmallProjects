def digitize(number: int, *, width: int = 10) -> list[int]:
    digits = [0] * width
    number = abs(number)
    index = -1
    while number:
        digits[index] = number % 10
        number //= 10
        index -= 1
    return digits


def sorobanize(digits: list[int]) -> tuple[list[int], list[int]]:
    fives = [digit // 5 for digit in digits]
    ones = [digit % 5 for digit in digits]
    return fives, ones


def soroban_image(number: int) -> str:
    def prepare(*, height: int) -> list[list[str]]:
        return [["I"] + (["|"] * width) + ["I"] for _ in range(height)]

    def glue() -> str:
        return "\n".join(" ".join(str(n) for n in line) for line in lines)

    digits = digitize(number)
    fives, ones = sorobanize(digits)
    width = len(digits)
    separator = f"+{'=' * (width * 2 + 1)}+"
    parts = [separator]
    lines = prepare(height=3)
    for x, n in enumerate(fives, 1):
        y = n * 2
        lines[y][x] = "O"
    parts += [glue(), separator]
    lines = prepare(height=6)
    for y in range(6):
        for x, n in enumerate(ones, 1):
            if (y - n) not in {0, 1}:
                lines[y][x] = "O"
    parts += [glue(), f"+={'='.join(str(n) for n in digits)}=+"]
    return "\n".join(parts)
