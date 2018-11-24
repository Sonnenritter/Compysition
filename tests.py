import unittest
from musicmath import Duration, Tone, Note, Chord, Rest, Melody, FullBarError
import helperfunctions as hf

N = Note
T = Tone
R = Rest
M = Melody
C = Chord
D = Duration


class TestDurationMethods(unittest.TestCase):
    def test_setup_empty(self):
        duration = D()
        self.assertEqual(str(duration), "1/4")

    def test_setup_with_kwarg1(self):
        duration = D(duration="3/4")
        self.assertEqual(str(duration), "3/4")

    def test_setup_with_kwarg2(self):
        duration = D(duration=(3, 4))
        self.assertEqual(str(duration), "3/4")

    def test_setup_with_arg1(self):
        duration = D("3/4")
        self.assertEqual(str(duration), "3/4")

    def test_setup_with_arg2(self):
        duration = D((3, 4))
        self.assertEqual(str(duration), "3/4")

    def test_add(self):
        duration1 = D((3, 4))
        duration2 = D((1, 5))
        duration3 = duration1 + duration2
        self.assertEqual(str(duration3), "19/20")


class TestToneMethods(unittest.TestCase):
    def test_setup_empty(self):
        tone = T(0)
        self.assertEqual(str(tone), "C-4")

    def test_setup_with_arg1(self):
        tone = T(1)
        self.assertEqual(str(tone), "Cis-4")

    def test_setup_with_arg2(self):
        tone = T(1, 5)
        self.assertEqual(str(tone), "Cis-5")

    def test_setup_with_kwarg(self):
        tone = T(value=1, octave=5)
        self.assertEqual(str(tone), "Cis-5")

    def test_add(self):
        tone1 = T(value=1, octave=5)
        tone2 = T(value=2, octave=5)
        tone3 = tone1 + tone2
        self.assertEqual(str(tone3), "Dis-5")

    def test_add2(self):
        tone1 = T(value=11, octave=5)
        tone2 = T(value=11, octave=5)
        tone3 = tone1 + tone2
        self.assertEqual(str(tone3), "Ais-5")


class TestRestMethods(unittest.TestCase):
    def test_setup_empty(self):
        rest = R()
        self.assertEqual(str(rest), '1/4 rest')

    def test_setup_with_arg(self):
        rest = R("4/4")
        self.assertEqual(str(rest), '1/1 rest')


class TestNoteMethods(unittest.TestCase):
    def test_setup_empty(self):
        note = N()
        self.assertEqual(str(note), "1/4 C-4")

    def test_setup_with_arg(self):
        note = N(1, (2, 4), 5)
        self.assertEqual(str(note), "1/2 Cis-5")

    def test_setup_with_kwarg(self):
        note = N(value=1, duration=(2, 4), octave=5)
        self.assertEqual(str(note), "1/2 Cis-5")

    def test_add(self):
        note1 = N(1)
        note2 = N(1)
        note3 = note1 + note2
        self.assertEqual(str(note3), "1/2 D-4")

    def test_equal1(self):
        note1 = N(1)
        note2 = N(2)
        self.assertEqual(note1 == note2, False)

    def test_equal2(self):
        note1 = N(1)
        note2 = N(1)
        self.assertEqual(note1 == note2, True)

    def test_equal3(self):
        n1 = N(1, duration=(1, 3))
        n2 = N(1)
        self.assertEqual(n1 == n2, False)


class TestChordMethods(unittest.TestCase):
    def test_setup_empty(self):
        chord = C([T(0), T(4), T(7)])
        self.assertEqual(str(chord), "1/4 C-4,E-4,G-4")

    def test_setup_empty_with_arg0(self):
        chord = C([T(2)])
        self.assertEqual(str(chord), "1/4 D-4")

    def test_setup_empty_with_arg1(self):
        chord = C([T(2, 5), T(1, 6), T(11)])
        self.assertEqual(str(chord), "1/4 D-5,Cis-6,H-4")

    def test_setup_empty_with_arg2(self):
        chord = C([T(2, 5), T(1, 6), T(11)], "3/4")
        self.assertEqual(str(chord), "3/4 D-5,Cis-6,H-4")

    def test_setup_with_tone_list(self):
        tones = [T(0), T(2), T(4)]
        chord = C(tones)
        self.assertEqual(str(chord), "1/4 C-4,D-4,E-4")

    def test_setup_with_note_list(self):
        notes = [N(0), N(2), N(4)]
        chord = C(notes)
        self.assertEqual(str(chord), "1/4 C-4,D-4,E-4")

    # def test_add(self):
    #    tones = [Tone('C'), Tone('D'), Tone('E')]
    #    chord = Chord(tones)
    #    chord = chord + 'G'
    #    self.assertEqual(str(chord), "1/4 C-4,D-4,E-4,G-4")

    def test_setup_with_two_same_tones(self):
        notes = [N(0), N(4), N(4)]
        chord = C(notes)
        self.assertEqual(str(chord), "1/4 C-4,E-4")


class TestMelodyMethods(unittest.TestCase):
    pass


class TestHelperfunctions(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
