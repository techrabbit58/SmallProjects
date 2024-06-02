import sys
import time

from . import rules
from .cards import Deck, Hand


def _exit(arg: int | None = None) -> None:
    print('\nBye! See you next time.')
    sys.exit(arg)


def _get_bet(money: int) -> int:
    print(f'You have {money} money.')
    bet = 0
    while True:
        try:
            answer = input('Your bet? (or q=quit) ')
            if answer == 'q':
                raise KeyboardInterrupt
            bet = int(answer)
        except ValueError:
            pass
        except KeyboardInterrupt:
            return -1
        if 1 <= bet <= money:
            break
        else:
            print("That wasn't a good number.")
            print(f'Please enter a number between 1 and {money}.')
            continue
    return bet


def _display_hands(*, dealer: Hand, player: Hand, hide_dealer: bool = True) -> None:
    print(dealer.score_to_str('DEALER', hide=hide_dealer))
    print(dealer.as_display_str(hide_first_card=hide_dealer))

    print(player.score_to_str('\nPLAYER'))
    print(player.as_display_str())

    print()


def _get_command(player: Hand, money: int) -> str:
    while True:
        choices = ['(q)uit', '(h)it', '(s)tand']
        answer = None
        if money > 0 and player.card_count() == 2:
            choices.append('(d)ouble down')
        try:
            answer = input(', '.join(choices) + '? ').lower()
        except KeyboardInterrupt:
            _exit()
        if answer in set('qhsd'):
            return answer


def gameloop() -> None:
    def support_player_actions() -> str | None:
        nonlocal bet
        while player.score() <= 21:
            _display_hands(dealer=dealer, player=player)
            command = _get_command(player, money - bet)
            if command == 'q':
                return 'quit'
            if command == 'd':  # try double down
                bet += min(bet, money - bet)
                print(f'You increased your bet to {bet} money.')
            if command in 'dh':  # did double down or hit
                new_card = deck.pop()
                print(f'You got the {new_card.rank} of {new_card.suit}.\n')
                player.add(new_card)
                continue
            if command in 'sd':  # stop this turn for the player
                break
        _display_hands(dealer=dealer, player=player)
        return None

    def conduct_dealer_actions():
        if dealer.score() > 21:
            return
        while dealer.score() < 17:
            print('Dealer hits ...')
            dealer.add(deck.pop())
            time.sleep(1)
            _display_hands(dealer=dealer, player=player)
            if dealer.score() > 21:  # The dealer busted.
                break

    def finish():
        nonlocal money
        dealer_score, player_score = dealer.score(), player.score()
        if dealer_score > 21:
            print(f'The dealer busted. You won {bet} money.')
            money += bet
        elif player_score > 21 or player_score < dealer_score:
            print(f'You lost {bet} money. The dealer won.')
            money -= bet
        elif dealer_score < player_score:
            print(f'You won {bet} money. The dealer lost.')
            money += bet
        else:  # Must be a tie
            print("It's a tie. You get your money back.")

    info, money = rules.to_display_str()

    print(info)

    while money > 0:
        bet = _get_bet(money)
        if bet < 0:
            break

        deck = Deck()
        dealer = Hand().add(deck.pop(), deck.pop())
        player = Hand().add(deck.pop(), deck.pop())

        if support_player_actions() == 'quit':
            break
        conduct_dealer_actions()
        _display_hands(dealer=dealer, player=player, hide_dealer=False)
        finish()

    if money == 0:
        print("You are broke. Good thing that the money you lost wasn't real.")

    print('Thank you for playing.')
    print('Bye!')
