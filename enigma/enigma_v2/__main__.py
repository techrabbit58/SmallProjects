from .enigma import EnigmaRocket

enigma = EnigmaRocket('III I II', '26 17 16 13')

enigma.set_key('JEZA')

cryptext = 'DEUTS QETRU PPENS INDJE TZTIN ENGLA ND---'
# cryptext = 'QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---'

print(cryptext)
print(''.join(enigma.convert(s) for s in cryptext))
