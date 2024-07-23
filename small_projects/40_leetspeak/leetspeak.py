import random

_charmap = dict(
    a=['4', '@', '/-\\'],
    c=['('],
    d=['|)'],
    e=['3'],
    f=['ph'],
    h=[']-[', '|-|'],
    i=['1', '!', '|'],
    k=['|<'],
    o=['0'],
    s=['$', '5'],
    t=['7', '+'],
    u=['|_|'],
    v=['\\/'],
)


def encode(text: str, likelihood: float) -> str:
    sequence = []

    for ch in text:
        encoded = ch

        if random.random() <= likelihood:
            encoded = random.choice(_charmap.get(ch.lower(), [ch]))

        sequence.append(encoded)

    return ''.join(sequence)
