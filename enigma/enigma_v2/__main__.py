from .enigma import EnigmaT
from .procedures import base64_encrypt, base64_decrypt, in_groups

enigma = EnigmaT('IV VIII V', '09 17 16 13')

key = 'QQEX'

casual_text = 'Bräsige Seelöwen heißen meistens Jürgen.'
print(casual_text)

ciphertext = in_groups(base64_encrypt(enigma, key, casual_text), group_size=4)
print(ciphertext)

plaintext = base64_decrypt(enigma, key, ciphertext)
print(plaintext)
