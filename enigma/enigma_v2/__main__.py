from .enigma import EnigmaA27

enigma = EnigmaA27('III I II', '26 17 16 13')

enigma.set_key('JEZA')

cryptext = 'QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---'

print(cryptext)
print(''.join(enigma.convert(s) for s in cryptext))
