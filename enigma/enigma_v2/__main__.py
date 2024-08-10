from .enigma import EnigmaRocket
from .procedures import casual_conversion
from .symbols import symbols_to_number_string

# cryptext = 'DEUTS QETRU PPENS INDJE TZTIN ENGLA ND---'
# cryptext = 'QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---'

enigma = EnigmaRocket('III I II', symbols_to_number_string('ZQPM'))
print('ring setting:', symbols_to_number_string('ZQPM'))

key = 'JEZA'
casual_text = 'Ukrainische Truppen sind jetzt in der russischen Region Kursk.'
print(casual_conversion(enigma, key, casual_text))
