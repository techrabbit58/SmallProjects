import time
from typing import TypeAlias

from .interaction import intro, ask_player
from .setup import (
    ENTER,
    QUIT,
    get_end_time,
    PLACES, TAXI,
    SUSPECTS,
    ITEMS,
    CULPRIT,
    MAX_ACCUSATIONS,
    PLACE_FIRST_LETTERS,
    LONGEST_PLACE_NAME_LENGTH,
)


Minutes: TypeAlias = int
Seconds: TypeAlias = int


def game_loop() -> None:
    print(intro())
    ask_player("Press Enter to begin ...", ENTER)

    current_place = TAXI
    visited_places = {}  # place -> (list of suspects, list of items)
    known_suspects_and_items = set()
    accused_suspects = set()  # Accused suspects won't offer clues.
    accusations_left = MAX_ACCUSATIONS
    end_time = get_end_time()

    is_terminated = False

    while not is_terminated:
        culprit_index = SUSPECTS.index(CULPRIT)
        place = PLACES[culprit_index]
        item = ITEMS[culprit_index]
        if result := is_game_over(end_time, accusations_left, CULPRIT, place, item):
            print(result)
            is_terminated = True
            continue

        minutes_left, seconds_left = get_remaining_period(end_time)
        print(f"Time left: {minutes_left} minutes, {seconds_left} seconds")

        if current_place == TAXI:
            print("\nYou are in your TAXI. Where do you want to go?")

            for place in sorted(PLACES):
                info = ""
                if place in visited_places:
                    info = visited_places[place]
                print(f"({place[0]}){place[1:]:<{LONGEST_PLACE_NAME_LENGTH + 3}}{info}")
            print("\nor (Q)uit game")
            while current_place == TAXI:
                answer, is_valid = ask_player("> ", {*PLACE_FIRST_LETTERS, QUIT})
                if not is_valid:
                    print(f"This is not a valid choice: \"{answer}\". Try again.")
                    continue
                if answer == "Q":
                    is_terminated = True
                    break
                current_place = next(filter(lambda s: s[0] == answer, PLACES))

            if is_terminated:
                continue

        print(f"\nYou are at the {current_place}.")
        print(dissect_current_place(current_place, visited_places, known_suspects_and_items))
        print()

        current_place = TAXI

        ask_player("Press Enter to continue ...", ENTER)
        print()

    print("\nThanks for playing!\n")


def dissect_current_place(current_place, visited_places, known_suspects_and_items) -> str:
    index = PLACES.index(current_place)
    local_suspect = SUSPECTS[index]
    local_item = ITEMS[index]
    info = f"{local_suspect} with the {local_item} is here."
    known_suspects_and_items.add(local_suspect)
    known_suspects_and_items.add(local_suspect)
    visited_places[current_place] = local_suspect.lower(), local_item.lower()
    return info


def is_game_over(end_time: float, accusations_left: int, culprit: str, place: str, item: str) -> str | None:
    result = [""]
    is_lost = False
    if accusations_left == 0:
        is_lost = True
        result.append("You have accused too many innocent people.")
    if end_time < time.time():
        is_lost = True
        result.append("You have run out of time.")
    if is_lost:
        result.append("")
        result.append(f"It was {culprit} at the {place} with the {item} who catnapped her.")
        result.append("Better luck next time, Detective!")
        return "\n".join(result)
    else:
        return None


def get_remaining_period(end_time: float) -> tuple[Minutes, Seconds]:
    now = time.time()
    time_left = int(end_time - now)
    minutes_left, seconds_left = time_left // 60, time_left % 60
    return minutes_left, seconds_left


game_loop()
