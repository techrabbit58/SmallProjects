import random
import sys
import time
from dataclasses import dataclass

from colterm import term

COLORS = "red green yellow blue purple cyan white".split()

WIDTH, HEIGHT = term.size()
WIDTH -= 1

NUM_KELP = 2
NUM_FISH = 10
NUM_BUBBLERS = 1
FRAMES_PER_SECOND = 2

# Fish type left and right must always have the same length!
FISH_TYPES = [
    {"right": ["><>"], "left": ["<><"]},
    {"right": [">||>"], "left": ["<||<"]},
    {"right": [">))>"], "left": ["<((<"]},
    {"right": [">||o", ">||."], "left": ["o||<", ".||<"]},
    {"right": [">))o", ">))."], "left": ["o((<", ".((<"]},
    {"right": [">-==>"], "left": ["<==-<"]},
    {"right": [r">\\>"], "left": ["<//<"]},
    {"right": ["><)))*>"], "left": ["<*(((><"]},
    {"right": ["}-[[[*>"], "left": ["<*]]]-{"]},
    {"right": ["]-<)))b>"], "left": ["<d(((>-["]},
    {
        "right": ["_.-._.-^=>", ".-._.-.^=>", "-._.-._^=>", "._.-._.^=>"],
        "left": ["<=^-._.-._", "<=^.-._.-.", "<=^_.-._.-", "<=^._.-._."]
    },
    {"right": ["><##*>"], "left": ["<*##><"]},
]

LONGEST_FISH_LENGTH = max(len(fish["right"][0]) for fish in FISH_TYPES)

# The x and y position where a fish may run into the edge of the screen.
LEFT_EDGE = 0
RIGHT_EDGE = WIDTH - 1 - LONGEST_FISH_LENGTH
TOP_EDGE = 0
BOTTOM_EDGE = HEIGHT - 2

def random_color() -> str:
    return random.choice(COLORS)


def make_fish_colors(fish_length: int) -> list[str]:
    pattern = random.choice("random head-tail single".split())

    colors = [random_color() for _ in range(fish_length)] \
        if pattern == "random" else [random_color()] * fish_length

    if pattern == "head-tail":
        colors[0] = random_color()
        colors[-1] = random_color()

    return colors  # Whole fish has the same color.


def random_x() -> int:
    return random.randint(LEFT_EDGE, RIGHT_EDGE)


def pause(millis: int) -> None:
    for _ in range(millis):
        time.sleep(0.001)


@dataclass(kw_only=True)
class Fish:
    right: list[str]
    left: list[str]
    x: int
    y: int
    colors: list[str]
    h_speed: int
    v_speed: int
    time_to_hdir_change: int
    time_to_vdir_change: int
    going_right: bool
    going_down: bool

    @property
    def length(self) -> int:
        return len(self.right[0])


def make_one_fish() -> Fish:
    fish_type = random.choice(FISH_TYPES)

    return Fish(
        right=fish_type["right"],
        left=fish_type["left"],
        x=random.randint(LEFT_EDGE, RIGHT_EDGE),
        y=random.randint(TOP_EDGE, BOTTOM_EDGE),
        colors=make_fish_colors(len(fish_type["right"][0])),
        h_speed=random.randint(1, 6),
        v_speed=random.randint(5, 15),
        time_to_hdir_change=random.randint(10, 60),
        time_to_vdir_change=random.randint(2, 20),
        going_right=random.choice((True, False)),
        going_down=random.choice((True, False)),
    )


@dataclass(kw_only=True)
class Kelp:
    x: int
    segments: list[str]


def random_kelp_segments() -> list[str]:
    return [random.choice("()") for _ in range(random.randint(6, HEIGHT - 1))]


fishes = [make_one_fish() for _ in range(NUM_FISH)]
bubblers = [random_x() for _ in range(NUM_BUBBLERS)]
bubbles = []
kelps = [Kelp(x=random_x(), segments=random_kelp_segments()) for _ in range(NUM_KELP)]
step = 0


def simulate_next_step() -> None:
    ...


def clear_aquarium() -> None:
    ...


def show_aquarium():
    fish = fishes[(step - 1) % NUM_FISH]
    term.goto(fish.x, fish.y)
    for i, segment in enumerate(fish.right[0]):
        term.fg(fish.colors[i])
        print(" ", end="", flush=True)

    fish = fishes[step % NUM_FISH]
    term.goto(fish.x, fish.y)
    for i, segment in enumerate(fish.right[0]):
        term.fg(fish.colors[i])
        print(segment, end="", flush=True)


def main() -> None:
    global fishes, bubblers, bubbles, kelps, step

    term.bg("black")
    term.clear()
    term.hide_cursor()

    term.fg("white")
    term.goto(LEFT_EDGE, HEIGHT - 1)
    print("Fish Tank: Press Ctrl+C to quit.", end="")

    delay = 1000 // FRAMES_PER_SECOND  # in millis
    step = 1
    while True:
        simulate_next_step()
        show_aquarium()
        pause(delay)
        clear_aquarium()
        step += 1


try:
    main()
except KeyboardInterrupt:
    term.clear()
    term.show_cursor()
    term.deinit()
    sys.exit()
