import textwrap
from collections.abc import Iterable


def intro() -> str:
    return textwrap.dedent("""
    J'Accuse! (A Mystery Game)

    Inspired by Al Sweigart, from the "Small Projects" book:
    https://nostarch.com/big-book-small-python-projects.

    You are the world-famous detective Mathilde Camus.

    ZOPHIE THE CAT has gone missing, and you must sift through the clues.
    
    Suspects either always tell lies, or always tell the truth. Ask them
    about other people, places, and items to see if the details they give
    are truthful and consistent with your observations. Then you will know
    if their clue about ZOPHIE THE CAT is true or not.

    Will you find ZOPHIE THE CAT in time and accuse the guilty party?
    """)


def ask_player(prompt: str, expected: Iterable[str]) -> tuple[str, bool]:
    response = input(prompt).strip()
    answer = response.upper()
    return (answer, True) if answer in expected else (response, False)
