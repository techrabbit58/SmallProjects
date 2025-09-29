import argparse
import calendar
import datetime

from colterm import term


def main(prog: str) -> None:
    parser = argparse.ArgumentParser(prog=prog, description='Create a monthly calender for given date.')
    parser.add_argument(
        'date', help='the desired date as YYYY-MM-DD (default=today)', nargs='?',
        type=datetime.date.fromisoformat, default=datetime.date.today().isoformat())

    args = parser.parse_args()
    screen_width = min(78, term.width())
    column_width = ((screen_width - 1) // 7) - 1

    year, month, today, *_ = args.date.timetuple()

    print(f'{calendar.month_name[month]} {year}'.center(screen_width))

    print(' ' + ' '.join(f'{name:^{column_width}}' for name in calendar.weekheader(column_width).split()))

    print('+', end='')
    print(('-' * column_width + '+') * 7)

    for week in calendar.monthcalendar(year, month):
        print('|', end='')
        for day in week:
            if day == today:
                print(f' {day:<2}{" <--":<{column_width - 3}}', end='|')
                continue
            print(f'{" ":{column_width}}' if day == 0 else f' {day:<{column_width - 1}}', end='|')
        for _ in range(3):
            print('\n|', end='')
            print((' ' * column_width + '|') * 7, end='')
        print('\n+', end='')
        print(('-' * column_width + '+') * 7)


if __name__ == '__main__':
    main('month_calendar')
