from .enigma import EnigmaRocket


def test_with_authentic_cryptogram_turing_treatise():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Turing.27s_Treatise.2C_1940
    Message included in a document written by Alan Turing for new codebreaker recruits at Bletchley Park.
    """
    enigma = EnigmaRocket('III I II', '26 17 16 13')

    key = 'JEZA'
    crypttext = 'QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---'
    plaintext = 'DEUTS QETRU PPENS INDJE TZTIN ENGLA ND---'

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext
