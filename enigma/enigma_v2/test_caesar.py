from .caesar import Caesar, Rot13, Atbash, MonoalphabeticCipher


def test_caesar():
    wheel = Caesar('C')

    message = 'Meet me by the rose bushes tonight.'

    cryptotext = ''.join(wheel.encrypt(c) for c in message)
    assert cryptotext == 'Oggv og da vjg tqug dwujgu vqpkijv.'

    plaintext = ''.join(wheel.decrypt(c) for c in cryptotext)
    assert message == plaintext


def test_rot13():
    wheel = Rot13()

    message = 'Meet me by the rose bushes tonight.'

    cryptotext = ''.join(wheel.translate(c) for c in message)
    assert cryptotext == 'Zrrg zr ol gur ebfr ohfurf gbavtug.'

    plaintext = ''.join(wheel.translate(c) for c in cryptotext)
    assert message == plaintext


def test_atbash():
    wheel = Atbash()

    message = 'Meet me by the rose bushes tonight.'

    cryptotext = ''.join(wheel.translate(c) for c in message)
    assert cryptotext == 'Nvvg nv yb gsv ilhv yfhsvh glmrtsg.'

    plaintext = ''.join(wheel.translate(c) for c in cryptotext)
    assert message == plaintext


def test_monoalphabetic():
    wheel = MonoalphabeticCipher('MICHAELKOSTUVWXYZBDFGJNPQR')  # MICHAELKOHLHAAS

    message = 'Meet me by the rose bushes tonight.'

    cryptotext = ''.join(wheel.encrypt(c) for c in message)
    assert cryptotext == 'Vaaf va iq fka bxda igdkad fxwolkf.'

    plaintext = ''.join(wheel.decrypt(c) for c in cryptotext)
    assert message == plaintext
