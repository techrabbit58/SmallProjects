import random
import sys


def door(n: str) -> list[str]:
    return [
        '+------+',
        '|      |',
        f'|   {n}  |',
        '|      |',
        '|      |',
        '|      |',
        '+------+'
    ]


def goat() -> list[str]:
    return [
        '+------+',
        '|  ((  |',
        '|  oo  |',
        '| /_/|_|',
        '|    | |',
        '|GOAT|||',
        '+------+'
    ]


def car() -> list[str]:
    return [
        '+------+',
        '| CAR! |',
        '|    __|',
        '|  _/  |',
        '| /_ __|',
        "|   O  |",
        '+------+'
    ]


def show_doors(*doors: list[str]) -> None:
    doors = list(zip(*doors))
    print('\n'.join('  '.join(d) for d in doors))


def main() -> None:
    swap_wins = swap_losses = stay_wins = stay_losses = 0

    while True:
        print("Let's make a deal!")

        doors = [door(n) for n in '123']
        door_with_car = random.choice('123')
        choices = list('123')
        current_choice = None

        while True:
            show_doors(*doors)
            print('Pick a door 1, 2, or 3 (or "quit" to stop):')
            answer = input('> ').lower().strip()
            if len(answer) and 'quit'.startswith(answer):
                break
            elif len(answer) and answer in '123':
                current_choice = answer
                choices.remove(current_choice)
                break
            else:
                print('Bad input. Please try again.')

        if current_choice is None:
            total_stays = stay_wins + stay_losses
            total_swaps = swap_wins + swap_losses

            print('Swapping:     ', end='')
            print(f'{swap_wins} wins, {swap_losses} losses')
            print(f'success rate: {(0 if total_swaps == 0 else swap_wins / total_swaps):.2f}%')

            print('Not swapping: ', end='')
            print(f'{stay_wins} wins, {stay_losses} losses')
            print(f'success rate: {(0 if total_stays == 0 else stay_wins / total_stays):.2f}%')

            sys.exit()

        if current_choice == door_with_car:
            uncover = random.choice([ch for ch in '123' if ch != door_with_car])
        else:
            uncover = [ch for ch in '123' if ch not in {current_choice, door_with_car}][0]

        print(f'Door number {uncover} contains a goat.')
        doors[int(uncover) - 1] = goat()
        choices.remove(uncover)

        stay = False
        while True:
            show_doors(*doors)
            print('Do you want to swap doors? (yes/no):')
            answer = input('> ').lower().strip()
            if len(answer) and 'yes'.startswith(answer):
                current_choice = [ch for ch in choices if ch != current_choice][0]
                break
            elif len(answer) and 'no'.startswith(answer):
                stay = True
                break
            else:
                print('Bad input. Please try again.')

        doors = [(car() if d == door_with_car else goat()) for d in '123']

        show_doors(*doors)
        print(f'Your choice is {current_choice}. Door {door_with_car} has the car.')
        if door_with_car == current_choice:
            print('You won!')
            if stay:
                stay_wins += 1
            else:
                swap_wins += 1
        else:
            print('Sorry, you lost.')
            if stay:
                stay_losses += 1
            else:
                swap_losses += 1

        input('Press "Enter" to repeat ... ')


if __name__ == '__main__':
    main()
