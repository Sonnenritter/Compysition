import pdb
import helperfunctions as hf
from fractions import Fraction


class Duration:
    def __init__(self, duration=(1, 4), *args, **kwargs):
        self.duration = Fraction(1, 4)

        self.set_duration(duration)

        super().__init__(*args, **kwargs)

    def set_duration(self, duration):
        try:
            self.duration = Fraction(*duration)
        except TypeError:
            self.duration = Fraction(duration)

    def add_dur(self, other):
        new_duration = self.duration + other.duration
        return Duration(duration=new_duration)

    def __add__(self, other):
        return self.add_dur(other)

    def __str__(self):
        return hf.frac_to_str(self.duration)


class Articulation:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tone:
    CORRECT_TONE_VALUES = ['Ces', 'C', 'Cis', 'Des', 'D', 'Dis', 'Es', 'E', 'Eis', 'Fes', 'F', 'Fis', 'Ges', 'G', 'Gis',
                           'As',
                           'A', 'Ais', 'B', 'H', 'His']

    INT_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def __init__(self, value='C', octave=4, *args, **kwargs):
        self.value = 'C'
        self.set_value(value)
        self.octave = 0
        self.set_octave(octave)
        super().__init__(*args, **kwargs)

    def set_octave(self, octave):
        self.octave = int(octave)
        return

    def add_ton(self, other):
        new_value = hf.tone_int_to_str((self.int_value + other.int_value) % 12)
        new_tone = Tone(value=new_value, octave=self.octave)
        return new_tone

    def __add__(self, other):
        return self.add_ton(other)

    @property
    def int_value(self):
        return hf.tone_str_to_int(self.value)

    def set_value(self, value):
        value = value.capitalize()
        if value in self.CORRECT_TONE_VALUES:
            self.value = value
        else:
            raise InputError(value, "invalid value")

    def __str__(self):
        return str(self.value) + "-" + str(self.octave)


class Note(Duration, Tone):
    def __init__(self, value="C", duration=(1, 4), octave=4):
        super().__init__(value=value, duration=duration, octave=octave)

    def __str__(self):
        return hf.frac_to_str(self.duration) + " " + str(self.value) + "-" + str(self.octave)

    def add_note(self, other):
        new_note = Note(duration=self.add_dur(other).duration, value=self.add_ton(other).value)
        return new_note

    def __add__(self, other):
        return self.add_note(other)


class Chord(Duration):
    def __init__(self, tones=('C', 'E', 'G'), duration=(1, 4)):
        self.tones = []
        self.add_notes(tones)
        super(Chord, self).__init__(duration=duration)

    def set_notes(self, new_tones):
        self.tones = []
        self.add_notes(new_tones)

    def add_notes(self, new_tones):

        for tone in new_tones:
            if hasattr(tone, 'value') and hasattr(tone, 'octave'):
                new_tone = Tone(tone.value, tone.octave)
            else:
                new_tone = Tone(*tone)

            if any(x.value == new_tone.value and x.octave == new_tone.octave for x in self.tones):
                pass
            else:
                self.tones.append(new_tone)

    def add(self, other):
        pass

    def __add__(self, other):
        self.add_notes(other)


    def __str__(self):
        str_tones = ""
        for tone in self.tones:
            str_tones += (str(tone) + ",")
        str_tones = str_tones[:-1]
        return hf.frac_to_str(self.duration) + " " + str_tones


class Rest(Duration):
    def __init__(self, duration=(1, 4)):
        super(Rest, self).__init__(duration=duration)

    def __str__(self):
        return hf.frac_to_str(self.duration) + ' rest'


# class Bar:
#     def __init__(self, notes=None, metre="4/4", offset=(0, 4)):
#
#         self.metre = (4, 4)
#         self.set_metre(metre)
#
#         self.offset = Fraction(0, self.metre[1])
#         if offset:
#             self.set_offset(offset)
#         self.notes = []
#         if notes:
#             self.add_notes(notes)
#
#     def empty(self):
#         self.notes = []
#         self.metre = (4, 4)
#         self.set_offset((0, 0))
#
#     def set_offset(self, offset):
#         try:
#             self.offset = Fraction(*offset)
#         except TypeError:
#             self.offset = Fraction(*offset)
#
#     def calculate_overhang(self):
#         if self.empty_space() < 0:
#             return self.empty_space() - 1
#         else:
#             return 0, 0
#
#     def fill_end(self):
#         self.add_note(Rest(self.empty_space()))
#
#     def add_notes(self, notes):
#         if isinstance(notes, Note):
#             self.add_note(notes)
#             return
#         for note in notes:
#             self.add_note(note)
#         return
#
#     def add_note(self, note):
#         if type(note) != Note and type(note) != Chord and type(note) != Rest:
#             raise InputError(note, " Type is not Note, Chord or Rest")
#         if self.is_full():
#             raise FullBarError("Bar is full")
#         self.notes.append(note)
#
#     def pop(self, index=None):
#         if index:
#             return self.notes.pop(index)
#         else:
#             return self.notes.pop()
#
#     def empty_space(self, with_offset=True):
#         filled_space = self.filled_space(with_offset=with_offset)
#
#         return Fraction(*self.metre) - filled_space
#
#     def filled_space(self, with_offset=True):
#         fraction_sum = sum([el.duration for el in self.notes])
#         if with_offset:
#             fraction_sum += self.offset
#         return fraction_sum
#
#     def is_full(self):
#         return self.empty_space() <= 0
#
#     def is_overloaded(self):
#         overhang = self.calculate_overhang()
#
#     def is_empty(self):
#         filling = self.empty_space(with_offset=False)
#         return filling[1] == 0
#
#     def set_metre(self, metre):
#
#         """
#
#         :param metre:
#         :return:
#         """
#         num, dem = metre.split("/")
#         num = int(num)
#         dem = int(dem)
#         if dem != 2 and dem != 4 and dem != 8:
#             raise InputError(metre, " denominator is not 2, 4 or 8")
#         self.metre = (num, dem)
#
#     def shorten_until_fits(self):
#         pass
#
#     def __str__(self):
#         bar_string = ''
#         for note in self.notes:
#             bar_string += (str(note) + '-> ')
#
#         return '|' + str(self.metre[0]) + '/' + str(self.metre[1]) + '|' + bar_string[:-3]


class Melody:
    def __init__(self, notes):
        self.notes = []
        self.add_notes(notes)
        self.metres = []

    def add_notes(self, *notes):
        for note in notes:
            self.add_note(note)

    def add_note(self, note):
        if type(note) != Note and type(note) != Chord and type(note) != Rest:
            new_note = Note(note)
            self.notes.append(new_note)
            return
        self.notes.append(note)
        return

    def set_metre(self, metre=(4, 4), start_bar=0, end_bar=None):
        pass

    def is_valid_metre(self, metre):
        if len(metre) != 2:
            return False
        if metre[1] != 2 and metre[1] != 4 and metre[1] != 8:
            raise False
        return True

    def pop_note(self, index=None):
        if index:
            pass
        else:
            pass

    def insert_note(self, note):
        pass

    def get_note(self, index):
        pass

    def __str__(self):
        track_string = ''
        for note in self.notes:
            track_string += str(note)
        return track_string


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class FullBarError(Error):
    def __init__(self, msg):
        self.msg = msg

def noteinput():
    notes = input("first note set")
    notes = notes.split(',')
    notes = [Note(x) for x in notes]
    return  notes

def notiplyinput():
    notes_a = noteinput()
    notes_b = noteinput()

    ply = hf.notiply(notes_a, notes_b)
    for note in ply:
        print(str(note))
    again = input('again?')
    if again =='y':
        notiplyinput()

def notishift():
    notes_a = noteinput()
    notes_b = noteinput()

    while

def main():

   notiplyinput()


if __name__ == "__main__":
    main()
