def main(x_repeat: int = 19, y_repeat: int = 12) -> None:

    for y in range(y_repeat):

        for x in range(x_repeat):  # Top half
            print(r"/ \_", end="")
        print()

        for x in range(x_repeat):  # Bottom half
            print(r"\_/ ", end="")
        print()


main(y_repeat=3)
