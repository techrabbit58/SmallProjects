import random


def generate_shuffled_lottery_drums() -> list[list[int]]:
    decades = [
        list(range(1, 10)), list(range(10, 20)), list(range(20, 30)),
        list(range(30, 40)), list(range(40, 50)), list(range(50, 60)),
        list(range(60, 70)), list(range(70, 80)), list(range(80, 91))
    ]

    for decade in decades:
        random.shuffle(decade)

    return decades


def distribute(row: list[int]) -> list[int | None]:
    distributed_row: list[int | None] = [None] * 9
    for number in row:
        decade = 8 if number == 90 else number // 10
        distributed_row[decade] = number
    return distributed_row


def pick_a_row(decades: list[list[int]], candidates: list[int]) -> list[int | None]:
    candidate_decades = sorted(candidates[:5])
    row = []
    for index in candidate_decades:
        row.append(decades[index].pop())
    return distribute(row)


def pick_all_rows(decades: list[list[int]]) -> list[list[int | None]]:
    rows = []
    candidates = list(range(9))
    for _ in range(17):
        candidates = [(n + 1) % 9 for n in candidates]
        row = pick_a_row(decades, candidates)
        rows.append(row)
    row = pick_a_row(decades, [n for n, decade in enumerate(decades) if decade])
    rows.append(row)
    random.shuffle(rows)
    return rows


def main() -> None:
    decades = generate_shuffled_lottery_drums()
    all_rows = pick_all_rows(decades)
    for group in range(6):
        for group_row in range(3):
            print(group + 1, group_row + 1, all_rows[group * 3 + group_row])
        print()


if __name__ == "__main__":
    main()
