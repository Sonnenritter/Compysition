#!/usr/bin/env python3
import threading
import time
import fluidsynth
from ctypes import *


def play_note(chan, key, vel, length):
    def the_playing():
        fs.noteon(chan, key, vel)
        time.sleep(length)
        fs.noteoff(chan, key)

    th = threading.Thread(target=the_playing)
    th.start()
    return th


def play_dur(key: int):
    play_note(0, key, 30, 0.3)
    play_note(0, key + 4, 30, 0.3)
    play_note(0, key + 7, 30, 0.3)


def play_moll(key: int):
    play_note(0, key, 30, 0.3)
    play_note(0, key + 3, 30, 0.3)
    play_note(0, key + 7, 30, 0.3)


def play_modulochords(key: int):
    play_note(0, key - (key % 3), 30, 0.3)
    play_note(0, key + (key % 4), 30, 0.3)
    play_note(0, key + (key % 7), 30, 0.3)


def get_key(tone, octave):
    return 12 + tone + 12 * octave


if __name__ == "__main__":
    global sequencer, fs, mySeqID, synthSeqID, now
    fs = fluidsynth.Synth()
    # fs.start()
    # you might have to use other drivers:
    fs.start(driver="alsa", midi_driver="alsa_seq")

    # 20<key<109
    sfid = fs.sfload("nice-keys.sf2")
    fs.program_select(0, sfid, 0, 0)
    fs.program_select(1, sfid, 0, 0)  # use the same program for channel 2 for cheapness
    booly = True
    while (booly):
        usr_in = input("zahl oder q")
        if usr_in == "q":
            booly = False
        try:
            note = get_key(int(usr_in), 0)
            play_note(0, note, 60, 0.3)
        except ValueError:
            pass

    fs.delete()
