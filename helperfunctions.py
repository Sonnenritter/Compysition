from fractions import Fraction



dur=[0,2,4,5,7,9,11]
nat_moll=(0,2,3,5,7,8,10)
har_moll=(0,2,3,5,7,8,11)
mel_moll=(0,2,)


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




def notishift(a,b,shift=0):
    new_notes=[]
    n=0
    len_a=len(a)
    len_b=len(b)
    notes_lcm= lcm(len_a,len_b)
    while(n<notes_lcm):
        new_notes.append(a[n%len_a] + b[(n+shift)%len_b])
        n+=1
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

