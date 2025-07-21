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


def main() -> None:
    digits = digitize(1364193)
    fives, ones = sorobanize(digits)
    width = len(digits)
    lines = [["I"] + (["|"] * width) + ["I"] for _ in range(3)]
    print(f"+{'=' * (width * 2 + 1)}+")
    for i, n in enumerate(fives):
        j = n * 2
        lines[j][i + 1] = "O"
    print("\n".join(" ".join(str(n) for n in line) for line in lines))
    print(f"+{'=' * (width * 2 + 1)}+")
    lines = [["I"] + (["|"] * width) + ["I"] for _ in range(6)]
    print("\n".join(" ".join(str(n) for n in line) for line in lines))
    print(f"+{'=' * (width * 2 + 1)}+")


main()
