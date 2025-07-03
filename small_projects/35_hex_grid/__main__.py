import argparse


def main() -> None:

    parser = argparse.ArgumentParser(prog="hexgrid")
    parser.add_argument("--x_repeat",
                        metavar="N", type=int, default=19,
                        help="repeat the pattern horizontally N times")
    parser.add_argument("--y_repeat",
                        metavar="N", type=int, default=12,
                        help="repeat the pattern vertically N times")
    args = parser.parse_args()

    for y in range(args.y_repeat):
        print(r"/ \_" * args.x_repeat)  # Top half.
        print(r"\_/ " * args.x_repeat)  # Bottom half.


main()
