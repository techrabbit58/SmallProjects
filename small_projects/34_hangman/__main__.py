import sys

IMAGES = [
    [" +--+"] * 7,
    [" |  |"] * 7,
    "    |. O  |. O  |. O  |. O  |. O  |. O  |".split("."),
    "    |.    |. |  |./|  |./|\ |./|\ |./|\ |".split("."),
    "    |.    |.    |.    |.    |./   |./ \ |".split("."),
    ["    |"] * 7,
    ["====="] * 7,
]


def show_image(n: int) -> None:
    for image in IMAGES:
        print(image[n])


class App:
    def run(self) -> None:
        for n in range(7):
            show_image(n)
            input("press enter > ")


try:
    App().run()
except KeyboardInterrupt:
    sys.exit()
