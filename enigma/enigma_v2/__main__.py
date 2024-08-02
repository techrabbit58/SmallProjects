from . import plugboard
from .basics import SYMBOLS, as_symbol, as_signal
from .reflectors import reflectors
from .rotors import rotors, Rotor

jumpers = plugboard.populate('AN EZ HK IJ LR MQ OT PV SW UX')
barrels = [
    rotors['III'].set_ring('01').create().set_key('U'),
    rotors['VI'].set_ring('08').create().set_key('Z'),
    rotors['VIII'].set_ring('13').create().set_key('V'),
]
reflections = reflectors['B']

cryptext = 'STEU EREJ TANA FJOR DJAN STAN DORT QUAA ACCC VIER NEUN NEUN ZWOF AHRT ZWON ULSM XXSC HARN HORS THCO'


def rotate(rotary: list[Rotor]) -> None:
    left, middle, right = rotary[0], rotary[1], rotary[2]
    if middle.is_at_notch():
        middle.rotate()
        left.rotate()
    elif right.is_at_notch():
        middle.rotate()
    right.rotate()


plain = []
for s in cryptext:
    s = s.upper()
    if s not in SYMBOLS:
        plain.append(s)
    else:
        rotate(barrels)
        signal = as_signal(s)
        signal = jumpers(signal)
        for r in reversed(barrels):
            i = r.right[signal]
            signal = r.left.index(i)
        signal = reflections[signal]
        for r in barrels:
            i = r.left[signal]
            signal = r.right.index(i)
        signal = jumpers(signal)
        plain.append(as_symbol(signal))

print(cryptext)
print(''.join(plain))
