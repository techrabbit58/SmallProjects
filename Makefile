.PHONY: clean install

clean:
	pip uninstall colterm caesarcode sevseg -y

install:
	pip install ./colterm ./caesarcode ./sevseg

colterm: ./colterm/setup.py ./colterm/colterm/term.py ./colterm/colterm/__init__.py
	pip install ./colterm -U

caesarcode: ./caesarcode/setup.py ./caesarcode/caesarcode/caesarcode.py ./caesarcode/caesarcode/__init__.py
	pip install ./caesarcode -U

sevseg: ./sevseg/setup.py ./sevseg/sevseg/sevseg.py ./sevseg/sevseg/__init__.py
	pip install ./sevseg -U

requirements: requirements.txt
	pip install -r requirements.txt

update: colterm sevseg caesarcode requirements

dice_math:
	python -m small_projects.17_dice_math

dice_roller:
	python -m small_projects.18_dice_roller

digital_clock: sevseg
	python -m small_projects.19_digital_clock

digital_stream:
	python -m small_projects.20_digital_stream

monty_hall:
	python -m small_projects.48_monty_hall

dna:
	python -m small_projects.21_dna

ducklings:
	python -m small_projects.22_ducklings

etching:
	python -m small_projects.23_etching_drawer

factorfinder:
	python -m small_projects.24_factor_finder

fastdraw:
	python -m small_projects.25_fast_draw

fibonacci:
	python -m small_projects.26_fibonacci

periodictable:
	python -m small_projects.53_periodic_table_of_elements

rot13:
	python -m small_projects.61_rot13

vigenere:
	python -m small_projects.80_vigenere

simplecode:
	python -m small_projects.66_simple_substitution_cipher

piglatin:
	python -m small_projects.54_pig_latin
