import json
import pathlib
import random
import sys
from dataclasses import dataclass


@dataclass(slots=True)
class TrickQuestion:
    question: str
    answer: str
    accept: list[str]


def load_questionaire(name: str) -> list[TrickQuestion]:
    with (pathlib.Path(sys.argv[0]).parent / name).open() as fp:
        return [TrickQuestion(**item) for item in json.load(fp)]


def main():
    questions = load_questionaire('trick_questions.json')
    index = random.randrange(len(questions))
    item = questions[index]
    print(item.question)
    answer = input('Your answer> ').strip()
    print('You got it!' if answer in item.accept
          else f'You missed it. The right answer could have been: {random.choice(item.accept)}')


main()
