import random
import time

ENTER = ""

TIME_TO_SOLVE = 5  # The player has this many seconds time to solve the riddle.
MAX_ACCUSATIONS = 3  # The player may accuse upt to this number of people.


def get_end_time() -> float:
    start_time = time.time()
    end_time = start_time + TIME_TO_SOLVE
    return end_time


PLACES = [
    place.strip() for place in """
        ZOO
        OLD BARN
        DUCK POND
        CITY HALL
        HIPSTER CAFE
        BOWLING ALLEY
        VIDEO GAME MUSEUM
        UNIVERSITY LIBRARY
        ALBINO ALLIGATOR PIT
        """.strip().split("\n")
]
random.shuffle(PLACES)

PLACE_FIRST_LETTERS = {place[0] for place in PLACES}
LONGEST_PLACE_NAME_LENGTH = max(len(place) for place in PLACES)
TAXI = "TAXI"

SUSPECTS = [
    suspect.strip() for suspect in """
        DUKE HAUTDOG
        MAX POWERS
        BILL MONOPOLIS
        SENATOR SCHMEAR
        MRS. FEATHERTOSS
        DR. SPLICER
        RAFFLES THE CLOWN
        ESPRESSA TOFFEEPOT
        CECIL E. VANDERTON
    """.strip().split("\n")
]
random.shuffle(SUSPECTS)

ITEMS = [
    item.strip() for item in """
        FLASHLIGHT
        CANDLESTICK
        RAINBOW FLAG
        HAMSTER WHEEL
        VHS TAPE
        JAR OF PICKLES
        LEFT COWBOY BOOT
        PINK TUXEDO
        5 DOLLAR GIFT CARD
    """.strip().split("\n")
]
random.shuffle(ITEMS)

assert len(PLACES) == len(SUSPECTS), "even distribution of suspects to places must be possible"
assert len(PLACES) == len(ITEMS), "even distribution of items to places must be possible"
assert len(PLACES) == len(PLACE_FIRST_LETTERS), "all places must have unique first letters"

LIARS = set(random.sample(SUSPECTS, random.randint(3, 4)))
CULPRIT = random.choice(SUSPECTS)


def generate_truth_tellers_clues() -> dict[str, dict[str, str]]:
    clues = {}

    for i, interviewee in enumerate(SUSPECTS):
        if interviewee in LIARS: continue
        clues[interviewee] = {"debug_liar": False}

        for index, item in enumerate(ITEMS):
            clues[interviewee][item] = (
                PLACES[index]  # Tells where the item is
                if random.randint(0, 1) == 0  # or, sometimes:
                else SUSPECTS[index])  # Tells who has the item

        for index, suspect in enumerate(SUSPECTS):
            clues[interviewee][suspect] = (
                PLACES[index]  # Tells where the suspect is
                if random.randint(0, 1) == 0  # or, sometimes:
                else ITEMS[index])  # Tells which item she has

    return clues


def generate_liars_clues() -> dict[str, dict[str, str]]:
    clues = {}

    for i, interviewee in enumerate(SUSPECTS):
        if interviewee not in LIARS: continue
        clues[interviewee] = {"debug_liar": True}

        for index, item in enumerate(ITEMS):
            if random.randint(0, 1) == 0:
                while True:
                    clues[interviewee][item] = random.choice(PLACES)
                    if clues[interviewee][item] != PLACES[index]:
                        break
            else:
                while True:
                    clues[interviewee][item] = random.choice(SUSPECTS)
                    if clues[interviewee][item] != SUSPECTS[index]:
                        break

        for index, suspect in enumerate(SUSPECTS):
            if random.randint(0, 1) == 0:
                while True:
                    clues[interviewee][suspect] = random.choice(PLACES)
                    if clues[interviewee][suspect] != PLACES[index]:
                        break
            else:
                while True:
                    clues[interviewee][suspect] = random.choice(ITEMS)
                    if clues[interviewee][suspect] != ITEMS[index]:
                        break

    return clues


CLUES = {  # suspect -> dictionary of clues
    **generate_truth_tellers_clues(),
    **generate_liars_clues(),
}


def generate_zophie_clues() -> dict[str, str]:
    clues = {}

    for interviewee in random.sample(SUSPECTS, random.randint(3, 4)):
        kind_of_clue = random.randint(1, 3)

        match kind_of_clue:

            case 1:  # The suspect tells truth or not about who the cuplrit is.
                if interviewee not in LIARS:
                    clues[interviewee] = CULPRIT
                else:
                    while (a_suspect := random.choice(SUSPECTS)) == CULPRIT:
                        clues[interviewee] = a_suspect

            case 2:  # The suspect tells truth or not about where ZOPHIE is.
                actual_place = PLACES[SUSPECTS.index(CULPRIT)]
                if interviewee not in LIARS:
                    clues[interviewee] = actual_place
                else:
                    while (a_place := random.choice(PLACES)) == actual_place:
                        clues[interviewee] = a_place

            case 3:  # The suspect tells truth or not about what item near ZOPHIE is.
                actual_item = ITEMS[SUSPECTS.index(CULPRIT)]
                if interviewee not in LIARS:
                    clues[interviewee] = actual_item
                else:
                    while (an_item := random.choice(ITEMS)) == actual_item:
                        clues[interviewee] = an_item

    return clues


ZOPHIE_CLUES = generate_zophie_clues()  # suspect -> a suspect or place or item
