"""
The 7-segment display module encoding of symbols.
The symbols are composed of characters with this segment order:
      __  ← a
 f → |__| ← b (The middle segment is 'g'.)
 e → |__| ← c (Right to the 'c' segment is the decimal point.)
       d

The resulting symbols are represented by a 2D array, five characters, wide
three characters high.
"""
from datetime import datetime

from sevseg import hms_time_display

if __name__ == '__main__':
    from colterm import term
    import time
    while True:
        try:
            term.clear()
            term.hide_cursor()
            term.fg('cyan')
            now = datetime.now().time()
            print(hms_time_display(now.hour, now.minute, now.second))
            term.fg('white', bright=False)
            term.show_cursor()
            print('Press Ctrl+C to stop.')
            term.fg('reset')
            time.sleep(1)
        except KeyboardInterrupt:
            break
