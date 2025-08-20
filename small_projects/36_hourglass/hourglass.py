HOURGLASS = set()

for i in range(18, 37):
    HOURGLASS.add((i, 1))
    HOURGLASS.add((i, 23))

for i in range(1, 5):
    HOURGLASS.add((18, i))
    HOURGLASS.add((36, i))
    HOURGLASS.add((18, i + 19))
    HOURGLASS.add((36, i + 19))

for i in range(8):
    HOURGLASS.add((19 + i, 5 + i))
    HOURGLASS.add((35 - i, 5 + i))
    HOURGLASS.add((25 - i, 13 + i))
    HOURGLASS.add((29 + i, 13 + i))
