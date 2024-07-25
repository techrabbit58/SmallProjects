import csv
import io
import os
import sys
import textwrap


def load_data(data_file_name: str) -> list[list[str]]:
    with open(data_file_name, encoding='utf8') as f:
        data = io.StringIO(f.read())
    elements = list(csv.reader(data))
    return elements


def element_by_atomic_number(elements: list[list[str]], atomic_number: str) -> list[str] | None:
    for description in elements:
        if description[0] == atomic_number:
            return description

    return None


def element_by_symbol(elements: list[list[str]], symbol: str) -> list[str] | None:
    for description in elements:
        if description[1] == symbol:
            return description

    return None


def get_element_report(fields: list[str]) -> str:
    labels = [
        'Atomic Number', 'Symbol', 'Element', 'Origin of name', 'Group', 'Period', 'Atomic weight',
        'Density', 'Melting point', 'Boiling point', 'Specific heat capacity', 'Electronegativity',
        'Abundance in earth\'s crust'
    ]
    units = [
        '', '', '', '', '', '', 'u',
        'g/cm³', 'K', 'K', 'J/(g * K)', '',
        'mg/kg'
    ]
    lines = [
        f'{label:>26}: {field} {unit}'
        for label, field, unit in zip(labels, fields, units)
        if field != chr(8211) and set(field).isdisjoint(set('[]'))
    ]
    return '\n'.join(lines + [''])


def prompt(text: str) -> str | None:
    print(text)
    response = input('> ').strip().upper()
    if response in {'Q', 'QUIT'}:
        return 'QUIT'
    return response


def overview() -> str:
    return textwrap.dedent(
        """
                     Periodic Table of Elements
        
          1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
        1 H                                                  He
        2 Li Be                               B  C  N  O  F  Ne
        3 Na Mg                               Al Si P  S  Cl Ar
        4 K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
        5 Rb Sr Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I  Xe
        6 Cs Ba La Hf Ta W  Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn
        7 Fr Ra Ac Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og
        
                Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu
                Th Pa U  Np Pu Am Cm Bk Cf Es Fm Md No Lr
        """)


def main():
    print(overview())

    elements = load_data(os.path.dirname(sys.argv[0]) + '/periodictable.csv')

    while True:
        response = prompt('Enter a symbol or atomic number to examine, or (Q)uit to stop.\n'
                          'If you <Enter> nothing, an overview of symbols is shown.')

        if response == 'QUIT':
            return

        if response == '':
            print(overview())
            continue

        element = element_by_symbol(elements, response.capitalize()) or element_by_atomic_number(elements, response)

        if element is None:
            print('No data. Unknown element? Please try another.')
            continue

        print(get_element_report(element))


main()
