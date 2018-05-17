import pdb
import helperfunctions as hf


class Duration:
    def __init__(self, duration=(4, 4), *args, **kwargs):
        self.duration = (4, 4)
        self.set_duration(duration)

        super().__init__(*args, **kwargs)

    def set_duration(self, duration):
        if type(duration) == str:
            self.duration = hf.frac_str_to_tuple(duration)
            return
        else:
            if len(duration) != 2:
                raise Error
            self.duration = (int(duration[0]), int(duration[1]))
            return

    def add_dur(self, other):
        new_duration = hf.frac_add((self.duration, other.duration))
        return Duration(duration=new_duration)

    def __add__(self, other):
        return self.add_dur(other)

    def __str__(self):
        return hf.frac_tuple_to_str(self.duration)


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
        return hf.frac_tuple_to_str(self.duration) + " " + str(self.value) + "-" + str(self.octave)

    def add_note(self, other):
        new_note = Note(duration=self.add_dur(other).duration, value=self.add_ton(other).value)
        return new_note

    def __add__(self, other):
        return self.add_note(other)


class Chord(Duration):
    def __init__(self, tones=('C', 'E', 'G'), duration=(1, 4)):
        self.tones = []
        self.set_notes(tones)
        super(Chord, self).__init__(duration=duration)

    def set_notes(self, tones):
        for tone in tones:
            if hasattr(tone, 'value') and hasattr(tone, 'octave'):
                self.tones.append(Tone(tone.value, tone.octave))
            else:
                self.tones.append(Tone(*tone))

    def add(self,other):


    def __add__(self, other):
        pass
    def __str__(self):
        str_tones = ""
        for tone in self.tones:
            str_tones += (str(tone) + ",")
        str_tones = str_tones[:-1]
        return hf.frac_tuple_to_str(self.duration) + " " + str_tones


class Rest(Duration):
    def __init__(self, duration=(1, 4)):
        super(Rest, self).__init__(duration=duration)

    def __str__(self):
        return hf.frac_tuple_to_str(self.duration) + ' rest'


class Bar:
    def __init__(self, notes=None, metre="4/4", offset=None):

        self.metre = (4, 4)
        self.set_metre(metre)

        self.offset = (0, self.metre[1])
        if offset:
            self.set_offset(offset)
        self.notes = []
        if notes:
            self.add_notes(notes)

    def empty(self):
        self.notes = []
        self.metre = (4, 4)
        self.set_offset((0, 0))

    def set_offset(self, offset):
        self.offset = offset

    def calculate_overload(self):
        if self.empty_space()[1] < 0:
            return self.empty_space()[1] * -1, self.empty_space()[2]
        else:
            return 0, 0

    def fill_end(self):
        self.add_note(Rest((self.empty_space()[1], self.empty_space()[2])))

    def add_notes(self, notes):
        if isinstance(notes, Note):
            self.add_note(notes)
            return
        for note in notes:
            self.add_note(note)
        return

    def add_note(self, note):
        if type(note) != Note and type(note) != Chord and type(note) != Rest:
            raise InputError(note, " Type is not Note, Chord or Rest")
        if self.is_full():
            raise FullBarError("Bar is full")
        self.notes.append(note)

    def pop(self, index=None):
        if index:
            return self.notes.pop(index)
        else:
            return self.notes.pop()

    def empty_space(self, with_offset=True):
        filled_space = self.filled_space(with_offset=with_offset)
        place_to_spend = self.metre[0] * (self.metre[1] / filled_space[2])
        empty_space = 1 - filled_space[0], place_to_spend - filled_space[1], filled_space[2]
        return empty_space

    def filled_space(self, with_offset=True):
        dems = []
        nums = []
        if not self.notes:
            return 0.0, 0, self.metre[1]
        for note in self.notes:
            dems.append(note.duration[1])
            nums.append(note.duration[0])

        dems.append(self.metre[1])
        if with_offset:
            dems.append(self.offset[1])

        factors = hf.scm_factors(dems)
        scm = hf.smallest_common_multiple(dems)
        fill_sum = 0
        for n, num in enumerate(nums):
            num = num * factors[n]
            fill_sum += num
        if with_offset:
            fill_sum += self.offset[0] * factors[-1]
        filled_space = fill_sum / (self.metre[0] * factors[-2]), fill_sum, scm
        return filled_space

    def is_full(self):
        return self.empty_space()[1] <= 0

    def is_empty(self):
        filling = self.empty_space(with_offset=False)
        return filling[1] == 0

    def set_metre(self, metre):

        """

        :param metre:
        :return:
        """
        num, dem = metre.split("/")
        num = int(num)
        dem = int(dem)
        if dem != 2 and dem != 4 and dem != 8:
            raise InputError(metre, " denominator is not 2, 4 or 8")
        self.metre = (num, dem)

    def __str__(self):
        bar_string = ''
        for note in self.notes:
            bar_string += (str(note) + '-> ')

        return '|' + str(self.metre[0]) + '/' + str(self.metre[1]) + '|' + bar_string[:-3]


class Track:
    def __init__(self):
        self.bars = []

    def add_notes(self, notes):
        if type(notes) != Note and type(notes) != Chord and type(notes) != Rest and type(notes) != Bar and type(
                notes) != list:
            raise InputError(notes, "wrong Type")
        if type(notes) is list:
            self.handle_list_add(notes)
            return
        elif type(notes) is Bar:
            self.add_bar(notes)
            return
        else:
            self.add_note(notes)

    def handle_list_add(self, notes):
        for item in notes:
            if type(notes) != Note and type(notes) != Chord and type(notes) != Rest and type(notes) != Bar:
                raise InputError(notes, "wrong Type")
            if type(item) is Bar:
                self.add_bar(item)
                return
            else:
                self.add_note(item)
                return

    def add_bar(self, bar):
        if len(self.bars) == 0:
            self.bars.append(bar)
            return
        else:
            last_bar_filling = self.bars[-1].empty_space()
            if last_bar_filling[1] > 0:
                self.fill_end()
                self.bars.append(bar)
                return
            elif last_bar_filling[1] == 0:
                self.bars.append(bar)
                return
            elif last_bar_filling[1] < 0:
                filler_bar = Bar(metre=self.bars[-1].metre)
                filler_bar.set_offset(self.bars[-1])
                self.bars.append(bar)
                return

    def fill_end(self):
        self.bars[-1].fill_end()
        return

    def add_note(self, note):
        if len(self.bars) == 0:
            self.bars.append(Bar())
            self.bars[-1].add_note(note)
        last_bar_filling = self.bars[-1].empty_space()
        if last_bar_filling[1] < 0:
            new_last_bar = Bar(offset=self.bars[-1].calculate_overload())
            self.bars.append(new_last_bar)
            self.add_note(note)
            return
        elif last_bar_filling[1] == 0:
            self.bars.append(Bar(metre=self.bars[-1].metre))
            self.bars[-1].add_note(note)
            return
        elif last_bar_filling[1] > 0:
            self.bars[-1].add_note(note)
            return

    def pop_bar(self, index=None):
        if index:
            pass
        else:
            return self.bars.pop()


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


def main():
    print(hf.smallest_common_multiple([2, 3, 4, 6, 5]))
    print(hf.scm_factors([2, 3, 4, 6, 5]))

    b = Bar()
    n = Note("Cis", "1/4", 3)
    d = Note("Cis", "3/4", 3)
    b.add_notes(n)
    b.add_notes(n)
    b.add_notes(d)

    track = Track()
    track.add_notes(b)
    track.add_notes(Note('Cis', "3/4", 5))
    print(track)


if __name__ == "__main__":
    main()
