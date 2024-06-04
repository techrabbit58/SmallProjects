def to_display_str() -> tuple[str, int]:
    rules = """
Rules:
  Try to get as close to 21 without going over.
  Kings, Queens and Jacks are worth 10 points.
  Aces are worth 1 or 11 points.
  Cards 2 to 10 are worth their face value.
  On your first play you may double down to increase your bet.
  But you must hit at the same time and cannot stand on the first play.
  The game may end with a tie. Just in case, you get your bet payed back.
  If you win, the dealer adds your bet to your money.
  If the dealer wins, your bet gets taken from your money.
  You start with 5000 money.
  
Commands:
  (h)it - take another card
  (s)tand - stand with your hand and stop taking cards
  (d)ouble down - increase your bet (only acceptable with the first play)
  (q)uit - quit the game
    """
    return rules, 5_000
