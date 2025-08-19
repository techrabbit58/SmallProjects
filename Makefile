.PHONY: clean install

clean:
	pip uninstall colterm caesarcode sevseg -y

install:
	pip install ./colterm ./caesarcode ./sevseg

colterm: ./colterm/setup.py ./colterm/colterm/term.py ./colterm/colterm/__init__.py
	pip install ./colterm -U --use-pep517

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

digital_clock:
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

spongecase:
	python -m small_projects.72_spongecase

guessthenumber:
	python -m small_projects.31_guess_the_number

gullible:
	python -m small_projects.32_gullible

hacking:
	python -m small_projects.33_hacking

hangman:
	python -m small_projects.34_hangman

fourinarow:
	python -m small_projects.30_four_in_a_row

fishtank:
	python -m small_projects.27_fish_tank

forest:
	python -m small_projects.29_forest_fire_sim

hexgrid:
	python -m small_projects.35_hex_grid

flooder:
	python -m small_projects.28_flooder

mazerunner:
	python -m small_projects.44_maze_runner_2d

diceroller:
	python -m small_projects.46_dice_roll_simulator

ninetynine:
	python -m small_projects.50_ninety_nine_bottles

rainbow:
	python -m small_projects.58_rainbow

rockpaperscissors:
	python -m small_projects.59_rock_paper_scissors

hanoi:
	python -m small_projects.77_towers_of_hanoi

soroban:
	python -m small_projects.70_soroban

monte:
	python -m small_projects.75_three_card_monte

tictactoe:
	python -m small_projects.76_tic_tac_toe

waterbucket:
	python -m small_projects.81_water_bucket_puzzle

langtonsant:
	python -m small_projects.39_langtons_ant

jaccuse:
	python -m small_projects.38_j_accuse

conway:
	python -m small_projects.13_conways_game

text2speach:
	python -m small_projects.74_text_to_speech "Biologists are just a bunch of cells that talk about other cells."

shining:
	python -m small_projects.65_shining_carpet

soundmimic:
	python -m small_projects.71_sound_mimic

hourglass:
	python -m small_projects.36_hourglass
