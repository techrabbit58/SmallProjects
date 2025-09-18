import os
import random
import sys
import textwrap
import time

MAX_NUM_SNAILS = 8
MAX_NAME_LENGTH = 20
FINISH_LINE = 40


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


def intro():
    return textwrap.dedent("""
    The Snail Race
    
        @v  <--  a snail
    """)


def ask_for_int(prompt: str, *, limits: tuple[int, int] = None) -> int:
    while True:
        print(prompt)
        response = input("> ").strip()
        if response.isdecimal():
            answer = int(response)
            if (limits is None) or (limits and limits[0] <= answer <= limits[1]):
                return answer
            else:
                print(f"Your answer must be in the inclusive range {limits[0]}..{limits[1]}")


def ask_for_one_word(prompt: str, *, max_length: int) -> str:
    while True:
        print(prompt)
        response = input("> ").strip()
        if len(response):
            return response.split()[0].title()[:max_length]
        else:
            print("Enter something. Try again.")


def render_race_track(progress: dict[str, int], snails: list[str]) -> None:
    clear_screen()
    print("START" + (" " * (FINISH_LINE - 5)) + "FINISH")
    print("|" + (" " * (FINISH_LINE - 1)) + "|")
    for snail in snails:
        print(f"{' ' * progress[snail]}{snail}\n{'.' * progress[snail]}@v")


def main() -> None:
    print(intro())

    num_snails = ask_for_int(f"How many snails will race? (max = {MAX_NUM_SNAILS})", limits=(2, MAX_NUM_SNAILS))

    snails = []
    for i in range(num_snails):
        snail = None
        while not snail:
            snail = ask_for_one_word(f"Enter snail #{i + 1}'s name.", max_length=MAX_NAME_LENGTH)
            if snail in snails:
                print(f"Duplicate snail name. Try again")
                snail = None
                continue
        snails.append(snail)

    progress = {snail: 0 for snail in snails}
    time.sleep(0.5)

    winner = None
    while not winner:
        render_race_track(progress, snails)
        for i in range(random.randint(1, num_snails // 2)):
            a_snail = random.choice(snails)
            progress[a_snail] += 1
            if progress[a_snail] > FINISH_LINE:
                winner = a_snail
                continue
        time.sleep(0.1)

    render_race_track(progress, snails)

    print(f"\n* * *  {winner} wins.  * * *\n")


try:
    main()
except KeyboardInterrupt:
    pass
