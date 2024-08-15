import textwrap

from .scramblingdevice import EnigmaM4


def test_with_authentic_cryptogram_u264():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#U-264_.28Kapit.C3.A4nleutnant_Hartwig_Looks.29.2C_1942
    """
    enigma = EnigmaM4(
        'Bruno',
        'Beta II IV I', '01 01 01 22'
    ).set_jumpers('AT BL DF GJ HM NW OP QY RZ VX')

    key = 'VJNA'
    crypttext = textwrap.dedent("""
    NCZW VUSX PNYM INHZ XMQX SFWX WLKJ AHSH NMCO CCAK UQPM KCSM HKSE INJU SBLK
    IOSX CKUB HMLL XCSJ USRR DVKO HULX WCCB GVLI YXEO AHXR HKKF VDRE WEZL XOBA
    FGYU JQUK GRTV UKAM EURB VEKS UHHV OYHA BCJW MAKL FKLM YFVN RIZR VVRT KOFD
    ANJM OLBG FFLE OPRG TFLV RHOW OPBE KVWM UQFM PWPA RMFH AGKX IIBG
    """).strip()
    plaintext = textwrap.dedent("""
    VONV ONJL OOKS JHFF TTTE INSE INSD REIZ WOYY QNNS NEUN INHA LTXX BEIA NGRI
    FFUN TERW ASSE RGED RUEC KTYW ABOS XLET ZTER GEGN ERST ANDN ULAC HTDR EINU
    LUHR MARQ UANT ONJO TANE UNAC HTSE YHSD REIY ZWOZ WONU LGRA DYAC HTSM YSTO
    SSEN ACHX EKNS VIER MBFA ELLT YNNN NNNO OOVI ERYS ICHT EINS NULL
    """).strip()

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext


def test_with_authentic_cryptogram_scharnhorst_m3_compatible():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Scharnhorst_.28Konteradmiral_Erich_Bey.29.2C_1943
    Try to decrypt the Sharnhorst M3 example with M3 compatibility settings for the reflector and leftmost rotor.
    Cannot be made compatible with M3, reflector A or Enigma I with reflector A.
    """
    enigma = EnigmaM4(
        'Bruno',  # choose Thin B reflector for M3 compatibitily
        'Beta III VI VIII', '01 01 08 13'  # choose Beta and set Beta ring to 01 for M3 compatibility
    ).set_jumpers('AN EZ HK IJ LR MQ OT PV SW UX')

    key = 'AUZV'  # set "greek" wheel to A for M3 compatibility
    crypttext = textwrap.dedent("""
    YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR
    """).strip()
    plaintext = textwrap.dedent("""
    STEU EREJ TANA FJOR DJAN STAN DORT QUAA ACCC VIER NEUN NEUN ZWOF AHRT ZWON ULSM XXSC HARN HORS THCO
    """).strip()

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext
