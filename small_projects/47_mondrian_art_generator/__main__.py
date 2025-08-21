from . import artwork


def generate_mondrian() -> None:
    artwork.erase()
    artwork.generate_vertical_lines()
    artwork.generate_horizontal_lines()
    artwork.delete_some_lines()
    artwork.add_borders()
    artwork.paint_rectangles()
    artwork.draw()

    try:
        input("Press Enter for another work of art, or Ctrl-C to quit.")
    except KeyboardInterrupt:
        exit()


def main() -> None:
    while True:
        generate_mondrian()


main()
