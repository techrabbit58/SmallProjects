_parameters = {
    "WIDTH": 40,
    "HEIGHT": 20,
    "NUM_TELEPORTS": 2,
    "NUM_ROBOTS": 10,
    "NUM_DEAD_ROBOTS": 2,
    "NUM_WALLS": 100,
    "EMPTY": ".",
    "PLAYER": "@",
    "ROBOT": "R",
    "DEAD_ROBOT": "X",
    "WALL": chr(9617),
}

def get(key: str) -> str | int | None:
    return _parameters.get(key)
