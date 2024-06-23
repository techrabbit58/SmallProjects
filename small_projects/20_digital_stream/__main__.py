import random
import shutil
import time


def main():
    frame_rate = 10
    density = 2
    min_stream_length, max_stream_length = 6, 14

    non_blanks = list(range(min_stream_length, max_stream_length + 1))
    blanks = [0] * (len(non_blanks) * ((100 // density) - 1))
    stream_lengths = blanks + non_blanks
    width = shutil.get_terminal_size()[0] - 1
    control = [random.choice(stream_lengths) for _ in range(width)]
    delay = 1 / frame_rate

    while True:
        line = [' '] * width
        for i, val in enumerate(control):
            if val > 0:
                line[i] = random.choice('01')
                control[i] -= 1
            else:
                control[i] = random.choice(stream_lengths)
        print(''.join(line))
        try:
            time.sleep(delay)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
