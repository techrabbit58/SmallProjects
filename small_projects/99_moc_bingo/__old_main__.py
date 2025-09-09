import random

from reportlab.lib import colors
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def draw_bingo_card(fields: list[list[list[int | None]]], filename: str = "bingo.pdf") -> None:
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5

    # set title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 20 * mm, "Ninety Balls Bingo")

    # draw cards
    field_width = 9 * 20  # 9 Spalten à 20px
    field_height = 3 * 20  # 3 Zeilen à 20px
    start_y = height - 40 * mm

    for i, field in enumerate(fields):
        x_offset = (width - field_width) / 2
        y_offset = start_y - i * (field_height + 15)

        for row in range(3):
            for col in range(9):
                x = x_offset + col * 20
                y = y_offset - row * 20

                # set background color
                c.setFillColor(colors.whitesmoke)
                c.rect(x, y, 20, 20, fill=1)

                # draw grid
                c.setStrokeColor(colors.grey)
                c.rect(x, y, 20, 20, fill=0)

                # insert numbers
                num = field[col][row]
                if num:
                    c.setFont("Helvetica-Bold", 10)
                    c.setFillColor(colors.black)
                    c.drawCentredString(x + 10, y + 6, str(num))

    c.save()


def make_shuffled_decades() -> list[list[int]]:
    decades = [
        list(range(1, 10)), list(range(10, 20)), list(range(20, 30)),
        list(range(30, 40)), list(range(40, 50)), list(range(50, 60)),
        list(range(60, 70)), list(range(70, 80)), list(range(80, 91))
    ]

    for decade in decades:
        random.shuffle(decade)

    return decades


def partition_decades(decades: list[list[int]]) -> list[list[int]]:
    columns = []
    for i, decade in enumerate(decades):
        columns.append([])
        for _ in range(6):
            columns[i].append([decades[i].pop()])
        for j in range(6):
            if len(decades[i]):
                columns[i][j].append(decades[i].pop())
                columns[i][j].sort()
        columns[i].sort(key=len)
    return columns


def generate_distribution_key() -> list[list[int]]:
    groups = [[2] * 9 for _ in range(6)]
    num_singles = [3, 2, 2, 2, 2, 2, 2, 2, 1]
    decade_seq = list(range(1, 8))
    random.shuffle(decade_seq)
    decade_seq = [0] + decade_seq + [8]
    for d in decade_seq:  # decades
        for g in groups:  # groups
            if num_singles[d] > 0 and sum(g) > 15:
                g[d] = 1
                num_singles[d] -= 1
    random.shuffle(groups)
    return groups


def expand_decade_to_three(part: list[int | None]) -> None:
    while len(part) < 3:
        part.insert(random.randrange(len(part) + 1), None)


def distribute_number_groups(decades: list[list[int | None]], key) -> list[list[list[int | None]]]:
    fields = []
    for field_index in range(6):
        fields.append([])
        for decade in range(9):
            size = key[field_index][decade]
            if size == 1:
                fields[-1].append(decades[decade].pop(0))
            else:
                fields[-1].append(decades[decade].pop())
            expand_decade_to_three(fields[-1][-1])
    return fields


def main():
    shuffled_decades = make_shuffled_decades()
    partitioned_decades = partition_decades(shuffled_decades)
    distribution_key = generate_distribution_key()
    all_fields = distribute_number_groups(partitioned_decades, distribution_key)
    draw_bingo_card(all_fields)


main()
