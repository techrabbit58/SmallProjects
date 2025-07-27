from . import buckets


GOAL = 4


def main() -> None:
    desired = GOAL
    all_buckets = {8: desired, 5: 0, 3: 0}
    print(buckets.render(all_buckets))
    if size := buckets.get_level_match(all_buckets, 4):
        print(f"The {size}L bucket has the desired water level of {desired}L.")

main()