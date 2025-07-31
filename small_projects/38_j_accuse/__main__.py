import time
from typing import TypeAlias

from .interaction import intro, ask_player
from .setup import (
    ENTER,
    get_end_time,
    PLACES, TAXI,
    SUSPECTS,
    ITEMS,
    CULPRIT,
    MAX_ACCUSATIONS,
)


Minutes: TypeAlias = int
Seconds: TypeAlias = int


def main() -> None:
    print(intro())
    ask_player("Press Enter to begin ...", ENTER)

    current_place = TAXI
    visited_places = {}  # place -> (list of suspects, list of items)
    accused_suspects = set()  # Accused suspects won't offer clues.
    accusations_left = MAX_ACCUSATIONS
    end_time = get_end_time()

    while True:
        culprit_index = SUSPECTS.index(CULPRIT)
        place = PLACES[culprit_index]
        item = ITEMS[culprit_index]
        if result := is_game_over(end_time, accusations_left, CULPRIT, place, item):
            print(result)
            break

        minutes_left, seconds_left = get_remaining_period(end_time)
        print(f"Time left: {minutes_left} minutes, {seconds_left} seconds")

        ask_player("Press Enter to continue ...", ENTER)

    print("\nThanks for playing!\n")


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


main()
