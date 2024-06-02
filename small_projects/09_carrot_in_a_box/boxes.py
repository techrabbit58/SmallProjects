from textwrap import dedent


def box(color: str, status: str = 'closed') -> list[str]:
    s = color
    return [f'{row:14}' for row in {
        'closed': dedent(f"""
        
        
        
          ,_________
         /         /|
        +---------+ |
        |  {s:4}   | |
        |  BOX    |/
        '---------'
        """).splitlines(),
        'empty': dedent(f"""
           _________
          |         |
          |         |
          |_________|
         /         /|
        +---------+ |
        |   {s:4}  | |
        |   BOX   |/
        '---------'
        """).splitlines(),
        'carrot': dedent(f"""
           ___VV____
          |   VV    |
          |   VV    |
          |___||____|
         /    ||   /|
        +---------+ |
        |   {s:4}  | |
        |   BOX   |/
        '---------'
        """).splitlines()
    }[status]]


def two_boxes(left: str, right: str) -> str:
    boxes = zip(box(*(left.split())), box(*(right.split())))
    return '\n'.join(row for row in (' '.join(row) for row in boxes) if row.strip())
