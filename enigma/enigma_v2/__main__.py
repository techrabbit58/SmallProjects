from .enigma import EnigmaM3
from .procedures import base64_encrypt, base64_decrypt, in_groups

# cryptext = 'DEUTS QETRU PPENS INDJE TZTIN ENGLA ND---'
# cryptext = 'QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---'

enigma = EnigmaM3('C', 'VI V VIII', '17 16 13').set_jumpers('AB CD EF GH JK MN OP QR TU XZ')

key = 'QED'
casual_text = 'Deutsche Truppen sind jetzt in England.'
print(casual_text)

ciphertext = in_groups(base64_encrypt(enigma, key, casual_text), 4)
print(ciphertext)

plaintext = base64_decrypt(enigma, key, ciphertext)
print(plaintext)
