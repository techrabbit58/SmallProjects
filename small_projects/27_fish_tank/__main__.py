import random
import sys
import time
from dataclasses import dataclass

from colterm import term

COLORS = "red green yellow blue purple cyan white".split()

WIDTH, HEIGHT = term.size()
WIDTH -= 1

NUM_KELP = 5
NUM_FISH = 7
NUM_BUBBLERS = 1
FRAMES_PER_SECOND = 18

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
    pattern = random.choice("random random head-tail head-tail head-tail single".split())

    colors = [random_color() for _ in range(fish_length)] \
        if pattern == "random" else [random_color()] * fish_length

    if pattern == "head-tail":
        colors[0] = random_color()
        colors[-1] = random_color()

    return colors  # Whole fish has the same color.


def random_x() -> int:
    return random.randint(LEFT_EDGE, RIGHT_EDGE)


def pause(centisec: int) -> None:
    for _ in range(centisec):  # centisec * 1/100 of a second.
        time.sleep(0.01)


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
        y=random.randint(TOP_EDGE, BOTTOM_EDGE - 1),
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
    return [random.choice("()") for _ in range(random.randint(6, HEIGHT - 2))]


@dataclass
class Bubble:
    x: int
    y: int


fishes = [make_one_fish() for _ in range(NUM_FISH)]
bubblers = [random_x() for _ in range(NUM_BUBBLERS)]
kelps = [Kelp(x=random_x(), segments=random_kelp_segments()) for _ in range(NUM_KELP)]

bubbles: list[Bubble] = []
step = 0


def simulate_next_step() -> None:
    global bubbles

    for fish in fishes:

        if step % fish.h_speed == 0:
            if fish.going_right:
                if fish.x != RIGHT_EDGE:
                    fish.x += 1
                else:
                    fish.going_right = False
                    fish.colors.reverse()
            else:
                if fish.x != LEFT_EDGE:
                    fish.x -= 1
                else:
                    fish.going_right = True
                    fish.colors.reverse()

        fish.time_to_hdir_change -= 1
        if fish.time_to_hdir_change == 0:
            fish.time_to_hdir_change = random.randint(10, 60)
            fish.going_right = not fish.going_right

        if step % fish.v_speed == 0:
            if fish.going_down:
                if fish.y != (BOTTOM_EDGE - 1):
                    fish.y +=1
                else:
                    fish.going_down = False
            else:
                if fish.y != TOP_EDGE:
                    fish.y -= 1
                else:
                    fish.going_down = True

        fish.time_to_vdir_change -= 1
        if fish.time_to_vdir_change == 0:
            fish.time_to_vdir_change = random.randint(2, 20)
            fish.going_down = not fish.going_down

    for bubbler in bubblers:
        if random.randint(1, 5) == 1:
            bubbles.append(Bubble(x=bubbler, y=BOTTOM_EDGE))

    for bubble in bubbles:
        score = random.randint(1, 6)
        if score == 1 and bubble.x != LEFT_EDGE:
            bubble.x -= 1
        elif score == 2 and bubble.x != RIGHT_EDGE:
            bubble.x += 1

        bubble.y -= 1
        bubbles = [bubble for bubble in bubbles if bubble.y > TOP_EDGE]

    for kelp in kelps:
        for i, segment in enumerate(kelp.segments):
            if random.randint(1, 20) == 1:
                kelp.segments[i] = ")" if segment == "(" else "("


def clear_aquarium() -> None:

    for bubble in bubbles:
        term.goto(bubble.x, bubble.y)
        print(" ", end="", flush=True)

    for fish in fishes:
        term.goto(fish.x, fish.y)
        print(" " * fish.length, end="", flush=True)

    for kelp in kelps:
        for i, segment in enumerate(kelp.segments):
            term.goto(kelp.x, BOTTOM_EDGE - i - 1)
            print("  ", end="", flush=True)


def show_aquarium():

    term.fg("white")
    for bubble in bubbles:
        term.goto(bubble.x, bubble.y)
        print(random.choice("oO"), end="", flush=True)

    for fish in fishes:
        term.goto(fish.x, fish.y)

        image = fish.right[step % len(fish.right)] \
            if fish.going_right else fish.left[step % len(fish.left)]

        for i, segment in enumerate(image):
            term.fg(fish.colors[i])
            print(segment, end="", flush=True)

        term.fg("green")
        for kelp in kelps:
            for i, segment in enumerate(kelp.segments):
                term.goto(kelp.x + (0 if segment == "(" else 1), BOTTOM_EDGE - i - 1)
                print(segment, end="", flush=True)


def get_delay_time() -> int:
    return 100 // FRAMES_PER_SECOND  # in 1/100 of a second


def main() -> None:
    global fishes, bubblers, bubbles, kelps, step

    term.bg("black")
    term.clear()
    term.hide_cursor()

    term.fg("yellow")
    term.goto(LEFT_EDGE, BOTTOM_EDGE)
    print("#" * (WIDTH - 1), end="", flush=True)

    term.fg("white")
    term.goto(LEFT_EDGE, HEIGHT - 1)
    print("Fish Tank: Press Ctrl+C to quit.", end="", flush=True)

    delay = get_delay_time()

    step = 1
    while True:
        simulate_next_step()
        show_aquarium()
        pause(delay)
        clear_aquarium()
        step += 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        term.clear()
        term.show_cursor()
        term.deinit()
        sys.exit()
