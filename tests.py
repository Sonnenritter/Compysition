import unittest
from musicmath import Duration, Tone, Note, Chord, Rest, Bar, Track, FullBarError


class TestDurationMethods(unittest.TestCase):
    def test_setup_empty(self):
        duration = Duration()
        self.assertEqual(str(duration), "4/4")

    def test_setup_with_kwarg1(self):
        duration = Duration(duration="3/4")
        self.assertEqual(str(duration), "3/4")

    def test_setup_with_kwarg2(self):
        duration = Duration(duration=(3, 4))
        self.assertEqual(str(duration), "3/4")

    def test_setup_with_arg1(self):
        duration = Duration("3/4")
        self.assertEqual(str(duration), "3/4")

    def test_setup_with_arg2(self):
        duration = Duration((3, 4))
        self.assertEqual(str(duration), "3/4")

    def test_add(self):
        duration1 = Duration((3, 4))
        duration2 = Duration((1, 5))
        duration3 = duration1 + duration2
        self.assertEqual(str(duration3), "19/20")


class TestToneMethods(unittest.TestCase):
    def test_setup_empty(self):
        tone = Tone()
        self.assertEqual(str(tone), "C-4")

    def test_setup_with_arg1(self):
        tone = Tone('Cis')
        self.assertEqual(str(tone), "Cis-4")

    def test_setup_with_arg2(self):
        tone = Tone('Cis', 5)
        self.assertEqual(str(tone), "Cis-5")

    def test_setup_with_kwarg(self):
        tone = Tone(value='Cis', octave=5)
        self.assertEqual(str(tone), "Cis-5")

    def test_add(self):
        tone1 = Tone(value='Cis', octave=5)
        tone2 = Tone(value='D', octave=5)
        tone3 = tone1 + tone2
        self.assertEqual(str(tone3), "Dis-5")

    def test_add2(self):
        tone1 = Tone(value='H', octave=5)
        tone2 = Tone(value='H', octave=5)
        tone3 = tone1 + tone2
        self.assertEqual(str(tone3), "Ais-5")


class TestRestMethods(unittest.TestCase):
    def test_setup_empty(self):
        rest = Rest()
        self.assertEqual(str(rest), '1/4 rest')

    def test_setup_with_arg(self):
        rest = Rest("4/4")
        self.assertEqual(str(rest), '4/4 rest')


class TestNoteMethods(unittest.TestCase):
    def test_setup_empty(self):
        note = Note()
        self.assertEqual(str(note), "1/4 C-4")

    def test_setup_with_arg(self):
        note = Note("Cis", (2, 4), 5)
        self.assertEqual(str(note), "2/4 Cis-5")

    def test_setup_with_kwarg(self):
        note = Note(value="Cis", duration=(2, 4), octave=5)
        self.assertEqual(str(note), "2/4 Cis-5")

    def test_add(self):
        note1 = Note('Cis')
        note2 = Note('Cis')
        note3 = note1 + note2
        self.assertEqual(str(note3), "2/4 D-4")


class TestChordMethods(unittest.TestCase):
    def test_setup_empty(self):
        chord = Chord()
        self.assertEqual(str(chord), "1/4 C-4,E-4,G-4")

    def test_setup_empty_with_arg0(self):
        chord = Chord('D')
        self.assertEqual(str(chord), "1/4 D-4")

    def test_setup_empty_with_arg1(self):
        chord = Chord((('D', 5), ('Cis', 6), 'H'))
        self.assertEqual(str(chord), "1/4 D-5,Cis-6,H-4")

    def test_setup_empty_with_arg2(self):
        chord = Chord((('D', 5), ('Cis', 6), 'H'), "3/4")
        self.assertEqual(str(chord), "3/4 D-5,Cis-6,H-4")

    def test_setup_with_tone_list(self):
        tones = [Tone('C'), Tone('D'), Tone('E')]
        chord = Chord(tones)
        self.assertEqual(str(chord), "1/4 C-4,D-4,E-4")

    def test_setup_with_note_list(self):
        notes = [Note('C'), Note('D'), Note('E')]
        chord = Chord(notes)
        self.assertEqual(str(chord), "1/4 C-4,D-4,E-4")

    def test_add(self):
        tones = [Tone('C'), Tone('D'), Tone('E')]
        chord = Chord(tones)
        chord = chord + 'G'
        self.assertEqual(str(chord), "1/4 C-4,D-4,E-4,G-4")


class TestBarMethods(unittest.TestCase):
    def test_setup_empty(self):
        bar = Bar()
        self.assertEqual(str(bar), "|4/4|")

    def test_setup_with_single_note(self):
        note = Note('D')
        bar = Bar(note)

        self.assertEqual(str(bar), "|4/4|1/4 D-4")

    def test_setup_with_single_note_filling(self):
        note = Note('D')
        bar = Bar(note)
        self.assertEqual(bar.empty_space(), (0.75, 3, 4))

    def test_setup_with_note_list(self):
        notes = [Note('C'), Note('D'), Note('E')]
        bar = Bar(notes)
        self.assertEqual(str(bar), "|4/4|1/4 C-4-> 1/4 D-4-> 1/4 E-4")

    def test_setup_with_note_list_metre_and_offset(self):
        notes = [Note('C'), Note('D'), Note('E')]
        offset = (1, 4)
        metre = '3/4'
        with self.assertRaises(FullBarError) as cm:
            bar = Bar(notes=notes, metre=metre, offset=offset)
            print(bar.filled_space())
        exception = cm.exception
        self.assertEqual(exception.msg, "Bar is full")

    def test_setup_with_note_list_metre_and_offset1(self):
        notes = [Note('C'), Note('D'), Note('E')]
        offset = (1, 4)
        metre = '4/4'
        bar = Bar(notes=notes, metre=metre, offset=offset)
        self.assertEqual(str(bar), "|4/4|1/4 C-4-> 1/4 D-4-> 1/4 E-4")

    def test_pop(self):
        notes = [Note('C'), Note('D'), Note('E')]
        bar = Bar(notes=notes)
        note = bar.pop()
        self.assertEqual(str(bar), "|4/4|1/4 C-4-> 1/4 D-4")
        self.assertEqual(str(note), "1/4 E-4")

    def test_pop_with_index(self):
        notes = [Note('C'), Note('D'), Note('E')]
        bar = Bar(notes=notes)
        note = bar.pop(1)
        self.assertEqual(str(bar), "|4/4|1/4 C-4-> 1/4 E-4")
        self.assertEqual(str(note), "1/4 D-4")


if __name__ == '__main__':
    unittest.main()
