import textwrap

from .enigma import EnigmaI


def test_with_authentic_cryptogram_instruction_manual():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Enigma_Instruction_Manual.2C_1930
    """
    enigma = EnigmaI(
        'A',
        'II I III', '24 13 22'
    ).set_jumpers('AM FI NV PS TU WZ')

    key = 'ABL'
    crypttext = textwrap.dedent("""
    GCDSE AHUGW TQGRK VLFGX UCALX VYMIG MMNMF DXTGN VHVRM
    MEVOU YFZSL RHDRR XFJWC FHUHM UNZEF RDISI KBGPM YVXUZ
    """).strip()
    plaintext = textwrap.dedent("""
    FEIND LIQEI NFANT ERIEK OLONN EBEOB AQTET XANFA NGSUE
    DAUSG ANGBA ERWAL DEXEN DEDRE IKMOS TWAER TSNEU STADT
    """).strip()

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext
