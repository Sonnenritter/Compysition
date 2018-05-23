from fractions import Fraction


def tone_int_to_str(int_tone):
    return {
        0: 'C',
        1: 'Cis',
        2: 'D',
        3: 'Dis',
        4: 'E',
        5: 'F',
        6: 'Fis',
        7: 'G',
        8: 'Gis',
        9: 'A',
        10: 'Ais',
        11: 'H',
    }.get(int_tone, 'C')


def tone_str_to_int(str_tone):
    return {
        'Ces': 11,
        'C': 0,
        'Cis': 1,
        'Des': 1,
        'D': 2,
        'Dis': 3,
        'Es': 3,
        'E': 4,
        'Eis': 5,
        'Fes': 4,
        'F': 5,
        'Fis': 6,
        'Ges': 6,
        'G': 7,
        'Gis': 8,
        'Ais': 8,
        'A': 9,
        'As': 10,
        'B': 10,
        'H': 11,
        'His': 0,
    }.get(str_tone, 0)


def frac_to_str(fraction):
    fraction_string = str(fraction.numerator) + "/" + str(fraction.denominator)
    return fraction_string


