import pdb
import helperfunctions as hf
from fractions import Fraction
import play
import time
from typing import List
from exceptions import InputError
from threading import Thread


class Duration:
    def __init__(self, duration=(1, 4), *args, **kwargs):
        self.duration = None
        self.location = None
        self.set_duration(duration)
        self.offset = 0
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
        return self.frac_to_str()

    def __eq__(self, other):
        return self.duration == other.duration

    def frac_to_str(self):
        fraction_string = str(self.duration.numerator) + "/" + str(self.duration.denominator)
        return fraction_string

    def play(self):
        pass

    def stop(self):
        pass

    @property
    def distance(self):
        return self.duration


class Tone:
    CORRECT_TONE_VALUES = ['Ces', 'C', 'Cis', 'Des', 'D', 'Dis', 'Es', 'E', 'Eis', 'Fes', 'F', 'Fis', 'Ges', 'G', 'Gis',
                           'As',
                           'A', 'Ais', 'B', 'H', 'His']

    INT_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def __init__(self, value, octave=4, velocity=50, *args, **kwargs):
        self.tone = None
        self.set_value(value)
        self.octave = 0
        self.set_octave(octave)
        self.velocity = velocity
        super().__init__(*args, **kwargs)

    @property
    def int_value(self):
        return self.tone

    def set_octave(self, octave):
        self.octave = int(octave)
        return

    def add_tone(self, other):
        new_value = (self.int_value + other.int_value) % 12
        new_tone = Tone(value=new_value, octave=self.octave)
        return new_tone

    def __add__(self, other):
        return self.add_tone(other)

    def set_value_from_name(self, name_value: str):
        name_value = name_value.capitalize()
        if name_value in self.CORRECT_TONE_VALUES:
            self.tone = hf.tone_str_to_int(name_value)

    def set_value(self, value: int):
        value = value % 12
        if value in self.INT_VALUES:
            self.tone = value
        else:
            raise InputError(value, "invalid value")

    def __str__(self):
        return str(hf.tone_int_to_str(self.tone)) + "-" + str(self.octave)

    def __eq__(self, other):
        return self.tone == other.int_value and self.octave == other.octave


class Note(Duration, Tone):
    def __init__(self, value=0, duration=(1, 4), octave=4, velocity=60):
        super().__init__(value=value, duration=duration, octave=octave, velocity=velocity)

    def __str__(self):
        return self.frac_to_str() + " " + str(hf.tone_int_to_str(self.tone)) + "-" + str(self.octave)

    def add_note(self, other):
        new_note = Note(duration=self.add_dur(other).duration, value=self.add_tone(other).tone)
        return new_note

    def __add__(self, other):
        return self.add_note(other)

    def play(self, ):
        play.play_note(self.int_value, self.octave, self.velocity, )

    def stop(self):
        play.stop_note(self.int_value, self.octave)

    def play_stop(self, tempo):
        self.play()
        time.sleep((tempo / 60) * float(self.duration))
        self.stop()

    def __eq__(self, other):
        return Tone.__eq__(self, other) and Duration.__eq__(self, other)


class Chord(Duration):
    def __init__(self, tones: List[Tone], duration=(1, 4)):
        self.tones = []
        self.add_notes(tones)

        super(Chord, self).__init__(duration=duration)

    def set_notes(self, new_tones):
        self.tones = []
        self.add_notes(new_tones)

    def add_notes(self, new_tones):

        for tone in new_tones:
            new_tone = Tone(tone.value, tone.octave)
            if new_tone not in self.tones:
                self.tones.append(new_tone)

    def __add__(self, other):
        self.add_notes(other)

    def __str__(self):
        str_tones = ""
        for tone in self.tones:
            str_tones += (str(tone) + ",")
        str_tones = str_tones[:-1]
        return self.frac_to_str() + " " + str_tones

    def play(self):
        for tone in self.tones:
            play.play_note(tone.int_value, tone.octave, tone.velocity)

    def stop(self):
        for tone in self.tones:
            play.stop_note(tone.int_value, tone.octave)

    def play_stop(self, tempo):
        self.play()
        time.sleep((tempo / 60) * float(self.duration))
        self.stop()


class Rest(Duration):
    def __init__(self, duration=(1, 4)):
        super(Rest, self).__init__(duration=duration)

    def __str__(self):
        return self.frac_to_str() + ' rest'


class Melody:
    def __init__(self, notes: List[Duration]):
        self.notes = []
        self.add_notes(notes)
        self.metres = []
        self.length = 0
        self.update_length()
        self.set_notes_offset()

    def set_notes_offset(self):
        for n, note in enumerate(self.notes):
            note.offset = hf.get_distance_between_items(0, n, self.notes)
            print(note.offset)

    def add_notes(self, notes):
        for note in notes:
            self.add_note(note)
        self.update_values()

    def update_values(self):
        self.update_length()
        self.set_notes_offset()

    def update_length(self):
        self.length = hf.get_whole_distance_from_distance_list(self.notes)

    def add_note(self, note: Duration):
        self.notes.append(note)

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

    def play(self, tempo):
        play_note_list(self.notes, tempo)

    def return_interval_with_offset(self, start: Fraction, stop: Fraction):
        offset, interval = hf.get_interval_with_offset(start, stop, self.notes)
        interval.insert(0, Duration(offset))
        return interval

    def __str__(self):
        track_string = ''
        for note in self.notes:
            track_string += str(note)
        return track_string


class Piece:
    def __init__(self, melodies: List[Melody]):
        self.melodies = melodies
        self.step_size = Fraction(2)
        self.current_step = Fraction(0)
        self.last_step = Fraction(0)
        self.length = max(melody.length for melody in self.melodies)
        self.command_list = []

    def make_ready_to_play(self):
        unsorted_commands = []
        for melody in self.melodies:
            melody.update_values()
            for note in melody.notes:
                unsorted_commands.extend(play.note_to_commands(note))

        self.command_list = sorted(unsorted_commands, key=lambda k: k.offset)

        for command in self.command_list:
            print(command.offset)

    def play(self, tempo):
        with play.Player() as player:
            for n, command in enumerate(self.command_list):
                command.run()
                if n < len(self.command_list)-1:
                    next_offset = self.command_list[n + 1].offset - command.offset
                    time.sleep((tempo / 60) * float(next_offset))


def play_note_list(notes: List[Duration], tempo):
    if 0 >= tempo:
        raise InputError(tempo, "tempo to small")
    for note in notes:
        note.play()
        time.sleep((tempo / 60) * float(note.duration))

        note.stop()


def note_input():
    notes = input("first note set")
    notes = notes.split(',')
    notes = [Note(x) for x in notes]
    return notes


def notiply_input():
    notes_a = note_input()
    notes_b = note_input()

    ply = hf.notiply(notes_a, notes_b)
    for note in ply:
        print(str(note))
    again = input('again?')
    if again == 'y':
        notiply_input()


def notishift_input():
    notes_a = note_input()
    notes_b = note_input()
    shift = int(input("shift"))
    notishift = hf.notishift(notes_a, notes_b, shift)
    for note in notishift:
        print(str(note))
    again = input('again?')
    if again == 'y':
        notishift_input()
