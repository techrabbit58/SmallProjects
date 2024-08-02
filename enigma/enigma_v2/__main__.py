from .rotors import rotors


print(rotors['V'].set_ring('02').create())
print(rotors['V'].create().set_key('B'))
print(rotors['V'].set_ring('02').create().set_key('B'))
