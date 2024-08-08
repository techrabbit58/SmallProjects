import textwrap

from .enigma import EnigmaM3


def test_with_authentic_cryptogram_sharnhorst():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Scharnhorst_.28Konteradmiral_Erich_Bey.29.2C_1943
    """
    enigma = EnigmaM3(
        'B',
        'III VI VIII', '01 08 13'
    ).set_jumpers('AN EZ HK IJ LR MQ OT PV SW UX')

    key = 'UZV'
    crypttext = 'YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR'
    plaintext = 'STEU EREJ TANA FJOR DJAN STAN DORT QUAA ACCC VIER NEUN NEUN ZWOF AHRT ZWON ULSM XXSC HARN HORS THCO'

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext


def test_with_authentic_cryptogram_instruction_manual():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Enigma_Instruction_Manual.2C_1930
    """
    enigma = EnigmaM3(
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


def test_with_authentic_cryptogram_barbarossa():
    """
    reference:
    http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages#Operation_Barbarossa.2C_1941
    """
    enigma = EnigmaM3(
        'B',
        'II IV V', '02 21 12'
    ).set_jumpers('AV BS CG DL FU HZ IN KM OW RX')

    key = 'BLA'
    crypttext = textwrap.dedent("""
    EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ REZKM LXLVE FGUEY
    SIOZV EQMIK UBPMM YLKLT TDEIS MDICA GYKUA CTCDO MOHWX
    MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ VIJHI DISHP RKLKA
    YUPAD TXQSP INQMA TLPIF SVKDA SCTAC DPBOP VHJK-
    """).strip()
    plaintext = textwrap.dedent("""
    AUFKL XABTE ILUNG XVONX KURTI NOWAX KURTI NOWAX NORDW
    ESTLX SEBEZ XSEBE ZXUAF FLIEG ERSTR ASZER IQTUN GXDUB
    ROWKI XDUBR OWKIX OPOTS CHKAX OPOTS CHKAX UMXEI NSAQT
    DREIN ULLXU HRANG ETRET ENXAN GRIFF XINFX RGTX-
    """).strip()

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext

    key = 'LSD'
    crypttext = textwrap.dedent("""
    SFBWD NJUSE GQOBH KRTAR EEZMW KPPRB XOHDR OEQGB BGTQV
    PGVKB VVGBI MHUSZ YDAJQ IROAX SSSNR EHYGG RPISE ZBOVM
    QIEMM ZCYSG QDGRE RVBIL EKXYQ IRGIR QNRDN VRXCY YTNJR
    """).strip()
    plaintext = textwrap.dedent("""
    DREIG EHTLA NGSAM ABERS IQERV ORWAE RTSXE INSSI EBENN
    ULLSE QSXUH RXROE MXEIN SXINF RGTXD REIXA UFFLI EGERS
    TRASZ EMITA NFANG XEINS SEQSX KMXKM XOSTW XKAME NECXK
    """).strip()

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in crypttext) == plaintext

    enigma.set_key(key)
    assert ''.join(enigma.convert(s) for s in plaintext) == crypttext
