import textwrap

from . import buckets


GOAL = 4


def advice(goal: int) -> str:
    return textwrap.dedent(f"""
    The Water Bucket Puzzle

    Try to get {goal}L of water into one of these buckets:
    
    You can:
    (F)ill one bucket
    (E)mpty one bucket
    (P)our one bucket into another
    (H)elps by showing this advice once more
    (Q)uit
    
    Examples: 
    "F 8" fills the 8L bucket. 
    "P 8 3" pours as much water as possible from 8L to 3L.
    """)


def main() -> None:
    print(advice(GOAL))
    desired = GOAL
    all_buckets = {8: desired, 5: 0, 3: 0}
    print(buckets.render(all_buckets))
    if size := buckets.get_level_match(all_buckets, 4):
        print(f"The {size}L bucket has the desired water level of {desired}L.")

main()