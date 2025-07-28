import textwrap

AIR = " "
WATER = "W"


def render(all_buckets: dict[int, int]) -> str:
    num_buckets, max_size = len(all_buckets), max(all_buckets)
    lines = [[""] * num_buckets for _ in range(max_size + 2)]
    for bucket, (size, level) in enumerate(all_buckets.items()):
        if level > size:
            raise ValueError(f"water level {level} may be greater then size in bucket {size}L")
        if level < 0:
            raise ValueError(f"water level {level} may not be negative for bucket {size}L")
        for y in range(size, 0, -1):
            water = AIR if y > level else WATER
            lines[max_size - y][bucket] = f"{str(y):>3}|{water * 6}|"
        lines[max_size][bucket] = "   +------+"
        lines[max_size + 1][bucket] = f"   {str(size) + 'L':^8s}"
    return textwrap.dedent("\n".join("".join(line) for line in lines))


def get_level_match(all_buckets: dict[int, int], desired: int) -> int | None:
    bucket = None
    for size, actual in all_buckets.items():
        if actual == desired:
            bucket = size
    return bucket