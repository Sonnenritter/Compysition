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


def frac_str_to_tuple(fraction_string):
    a, b = fraction_string.split("/")
    return int(a), int(b)


def frac_tuple_to_str(fraction_tuple):
    fraction_string = str(fraction_tuple[0]) + "/" + str(fraction_tuple[1])
    return fraction_string


def frac_add(fractions):
    dems = [el[1] for el in fractions]
    nums = [el[0] for el in fractions]
    scm_f = scm_factors(dems)
    num_sum = 0
    for n, num in enumerate(nums):
        num_sum += num * scm_f[n]
    new_frac = num_sum, dems[0] * scm_f[0]
    return new_frac


def frac_diff(a, b):
    scm_f = scm_factors((a[1], b[1]))
    new_frac = a[0] * scm_f[0] - b[0] * scm_f[1], b[1] * scm_f[1]
    return new_frac


def scm_factors(numbers):
    factors = []
    scm = smallest_common_multiple(numbers)
    for number in numbers:
        factors.append(int(scm / number))
    return factors


def smallest_common_multiple(numbers):
    def is_smallest_common_multiple(possible_scm, numbers_to_check):
        for number in numbers_to_check:
            if possible_scm % number != 0:
                return False
        return True

    m = numbers[0]
    current_factor = 1
    scm = m
    while not is_smallest_common_multiple(scm, numbers):
        current_factor += 1
        scm = m * current_factor

    return scm


def notiply(a, b):
    new_notes = []
    for note in a:
        for othernote in b:
            new_notes.append(note + othernote)
    return new_notes
