colterm: ./colterm/setup.py ./colterm/colterm/term.py ./colterm/colterm/__init__.py
	pip install ./colterm -U

caesarcode: ./caesarcode/setup.py ./caesarcode/caesarcode/caesarcode.py ./caesarcode/caesarcode/__init__.py
	pip install ./caesarcode -U

sevseg: ./sevseg/setup.py ./sevseg/sevseg/sevseg.py ./sevseg/sevseg/__init__.py
	pip install ./sevseg -U

requirements: requirements.txt
	pip install -r requirements.txt

update: colterm sevseg caesarcode requirements

dice_math: colterm
	python -m small_projects.17_dice_math

dice_roller:
	python -m small_projects.18_dice_roller

digital_clock: sevseg colterm
	python -m small_projects.19_digital_clock

digital_stream:
	python -m small_projects.20_digital_stream

monty_hall: colterm
	python -m small_projects.48_monty_hall
