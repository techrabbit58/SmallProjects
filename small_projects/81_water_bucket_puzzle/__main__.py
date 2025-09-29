import textwrap

from pyparsing import CaselessKeyword, nums, Word, ParseException

from . import buckets

GOAL = 4
BUCKET_ARRANGEMENT = {8: 0, 5: 0, 3: 0}


action_fill = CaselessKeyword("F")
action_empty = CaselessKeyword("E")
action_pour = CaselessKeyword("P")

arg_bucket = Word(nums).set_parse_action(lambda t: int(t[0]))

cmd_help = CaselessKeyword("H")
cmd_quit = CaselessKeyword("Q")

cmd_fill = action_fill + arg_bucket
cmd_empty = action_empty + arg_bucket
cmd_pour = action_pour + (arg_bucket * 2)

command = cmd_help | cmd_quit | cmd_fill | cmd_empty | cmd_pour


def advice(goal: int) -> str:
    return textwrap.dedent(f"""
    The Water Bucket Puzzle

    Try to get {goal}L of water into one of the buckets:
    
    You can:
    (F)ill one bucket
    (E)mpty one bucket
    (P)our one bucket into another
    (H)elp by showing this advice once more
    (Q)uit
    
    Examples: 
    "F 8" fills the 8L bucket. 
    "P 8 3" pours as much water as possible from 8L to 3L.
    """)


def main() -> None:
    print(advice(GOAL))
    all_buckets = BUCKET_ARRANGEMENT.copy()
    steps = 0

    is_terminated = False
    while not is_terminated:
        print(buckets.render(all_buckets), end="\n\n")

        answer = input("> ").strip()
        if not answer:
            continue

        try:
            verb, *args = command.parse_string(answer, parse_all=True)
            if verb == "Q":
                is_terminated = True
            elif verb == "H":
                print(advice(GOAL))
            elif verb == "F":
                size = args[0]
                if size not in all_buckets:
                    print(f"This is not a valid target: {size}L. Try again.\n")
                else:
                    all_buckets[size] = size
                    steps += 1
            elif verb == "E":
                size = args[0]
                if size not in all_buckets:
                    print(f"This is not a valid bucket: {size}L. Try again.\n")
                else:
                    all_buckets[size] = 0
                    steps += 1
            else:  # verb == "P"
                s1, s2 = args
                if s1 not in all_buckets:
                    print(f"This is not a valid origin: {s1}L. Try again.\n")
                elif s2 not in all_buckets:
                    print(f"This is not a valid target: {s2}L. Try again.\n")
                else:
                    vol = min(s2 - all_buckets[s2], all_buckets[s1])
                    all_buckets[s2] += vol
                    all_buckets[s1] -= vol
                    steps += 1
        except ParseException:
            print(f"\"{answer}\" is not a valid command. Try again, or try \"H\".\n")

        if buckets.get_level_match(all_buckets, desired=GOAL):
            print(buckets.render(all_buckets), end="\n\n")
            print(f"Good job. You solved it in {steps} steps.")
            is_terminated = True

    print("Thanks for playing.")


if __name__ == '__main__':
    main()
