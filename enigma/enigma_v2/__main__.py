from .enigma import EnigmaM3

enigma = EnigmaM3('B', 'III VI VIII', '01 08 13').set_jumpers('AN EZ HK IJ LR MQ OT PV SW UX')

enigma.set_key('UZV')

cryptext = 'YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR'

print(cryptext)
print(''.join(enigma.convert(s) for s in cryptext))
