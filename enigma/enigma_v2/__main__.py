from .enigma import EnigmaM3

enigma = EnigmaM3('A', 'II I III', '24 13 22').set_jumpers('AM FI NV PS TU WZ')

enigma.set_key('ABL')

cryptext = ('GCDSE AHUGW TQGRK VLFGX UCALX VYMIG '
            'MMNMF DXTGN VHVRM MEVOU YFZSL RHDRR '
            'XFJWC FHUHM UNZEF RDISI KBGPM YVXUZ')

print(cryptext)
print(''.join(enigma.convert(s) for s in cryptext))
