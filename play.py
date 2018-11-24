#!/usr/bin/env python3
import threading
import time
import fluidsynth
from ctypes import *


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
        fs.program_select(0, sfid, 0, 0)
        fs.program_select(1, sfid, 0, 0)  # use the same program for channel 2 for cheapness

    def __exit__(self, exc_type, exc_val, exc_tb):
        fs.delete()
