from string import Template

from playsound3 import playsound

URL = Template("https://inventwithpython.com/sound${letter}.wav")


def main():
    for letter in "FASADASAFASS":
        print(letter)
        playsound(URL.substitute(letter=letter))


main()
