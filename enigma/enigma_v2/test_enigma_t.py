from .scramblingdevice import EnigmaT


def test_with_authentic_cryptogram_tirpitz():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Enigma_Tirpitz.2C_1944
    The reflector wheel is "settable" for ring and key, but cannot be replaced (only one "Umkehrwalze".)
    """
    enigma = EnigmaT('VI IV VII', '06 17 03 20')

    key = 'FQDC'
    crypttext = (
        'IRCYP XNVSF ERKMK MNJZZ ZTDBF/'
        'GMFBO JGADL KJSVG JKSGB JQFKU/'
        'FXWVS MWGKO CPKMQ KFDDR MRDSQ/'
        'OAOIU GAIRM ZZCBQ MEFMG ZVAOQ/'
        'QWJXN JENOF DBHVK'
    )
    plaintext = (
        'MOEGL ICHER WEISE AUFNA HMEAU/'
        'FTREF FPUNK TNURD URCHZ WOZER/'
        'STOER ERXMI TSPYE TEREM HERAN/'
        'SCHLI ESSEN VONZW OTORP EDOBO/'
        'OTENR ECHNE NQMFW'
    )

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext
