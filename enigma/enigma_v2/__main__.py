from .enigma import EnigmaRocket
from .procedures import casual_conversion

enigma = EnigmaRocket('III I II', '26 17 16 13')

enigma.set_key('JEZA')

cryptext = 'DEUTS QETRU PPENS INDJE TZTIN ENGLA ND---'
# cryptext = 'QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---'

print(casual_conversion(enigma, 'JEZA', 'Deutsqe Truppen sind jetzt in England.'))
