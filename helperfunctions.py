from fractions import Fraction
from exceptions import OutofBoundsError

dur = [0, 2, 4, 5, 7, 9, 11]
nat_moll = (0, 2, 3, 5, 7, 8, 10)
har_moll = (0, 2, 3, 5, 7, 8, 11)
mel_moll = (0, 2,)


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


def notishift(a, b, shift=0):
    new_notes = []
    n = 0
    len_a = len(a)
    len_b = len(b)
    notes_lcm = lcm(len_a, len_b)
    while n < notes_lcm:
        new_notes.append(a[n % len_a] + b[(n + shift) % len_b])
        n += 1
    return new_notes


def notiply(a, b):
    new_notes = []
    for note in a:
        for othernote in b:
            new_notes.append(note + othernote)
    return new_notes


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def get_whole_distance_from_distance_list(the_list) -> Fraction:
    whole_distance = Fraction(0)
    for item in the_list:
        whole_distance += Fraction(item.distance)
    return whole_distance


def get_item_index_next_point_from_distance_list(point: Fraction, the_list):
    w_d = get_whole_distance_from_distance_list(the_list)
    if w_d <= point:
        raise OutofBoundsError
    l = len(the_list)

    walked_distance = 0
    for n, item in enumerate(the_list):
        if walked_distance < point:
            walked_distance += item.distance
        else:
            return n
    raise OutofBoundsError


def get_item_index_before_point_from_distance_list(point: Fraction, the_list):
    w_d = get_whole_distance_from_distance_list(the_list)
    if 0 >= point:
        raise OutofBoundsError

    l = len(the_list)
    remaining_distance = w_d - the_list[-1].distance
    for n, item in enumerate(reversed(the_list)):
        if remaining_distance >= point:
            remaining_distance -= item.distance
        else:
            return len(the_list) - n - 1
    raise OutofBoundsError


def get_distance_between_items(index_a, index_b, the_list) -> Fraction:
    distance = 0
    for item in the_list[index_a:index_b]:
        distance += item.distance
    return Fraction(distance)


def get_item_next_point_from_distance_list(point: Fraction, the_list):
    index = get_item_index_next_point_from_distance_list(point, the_list)
    return the_list[index]


def get_interval_from_distance_list(start: Fraction, stop: Fraction, the_list):
    w_d = get_whole_distance_from_distance_list(the_list)
    if start > w_d:
        raise OutofBoundsError
    if stop < start:
        return []

    start_index = get_item_index_next_point_from_distance_list(start, the_list)
    print(start_index)
    stop_index = get_item_index_before_point_from_distance_list(stop, the_list)
    print(stop_index)
    return the_list[start_index:stop_index + 1]


def get_interval_with_offset(start: Fraction, stop: Fraction, the_list):
    interval = get_interval_from_distance_list(start, stop, the_list)
    dist_to_a = get_distance_between_items(0, start, the_list)
    offset = Fraction(dist_to_a - start)
    return offset, interval
