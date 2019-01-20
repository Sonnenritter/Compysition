#!/usr/bin/env python3
from fractions import Fraction
import fluidsynth
from ctypes import *


class PlayCommand:
    def __init__(self, function, offset:Fraction,arguments=None):
        self.function = function
        self.arguments = arguments
        self.offset=offset

    def run(self):
        self.function(*self.arguments)


def note_to_commands(note):

    com1 = PlayCommand(play_note, note.offset, [note.tone,note.octave,note.velocity] )
    com2 = PlayCommand(stop_note, note.offset+note.duration, [note.tone,note.octave] )
    return [com1,com2]



def get_key(tone, octave):
    return 12 + tone + 12 * octave


def play_note(tone, octave, vel):
    fs.noteon(0, get_key(tone, octave), vel)


def stop_note(tone, octave):
    fs.noteoff(0, get_key(tone, octave))


class Player:
    def __enter__(self):
        global sequencer, fs, mySeqID, synthSeqID, now
        fs = fluidsynth.Synth()
        # fs.start()
        # you might have to use other drivers:
        fs.start(driver="alsa", midi_driver="alsa_seq")

        # 20<key<109
        sfid = fs.sfload("nice-keys.sf2")
        fs.program_select(0, sfid, 0, 1)
        fs.program_select(1, sfid, 0, 1)  # use the same program for channel 2 for cheapness

    def __exit__(self, exc_type, exc_val, exc_tb):
        fs.delete()
