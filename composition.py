from musicmath import Note, Tone, Rest, Melody, Chord, Duration, Piece


N = Note
T = Tone
R = Rest
M = Melody
C = Chord
D = Duration
P = Piece


def main():

    m_list = []
    m_list.append(M([]))
    m_list.append(M([]))
    m_list.append(M([]))
    m_list.append(M([]))
    m_list.append(M([]))
    for i in range(0, 400):
        oct = 0
        if i == 30:
            oct += 1

        if i == 100:
            oct += 1
        if i == 120:
            oct += 1

        m_list[0].add_note(N(i, (1, i * i % 12 + 1), velocity=100 - i % 100, octave=oct % 4 + 3))
        m_list[1].add_note(N(i + 4 * i, (2, i * (i + 1) % 12 + 1), velocity=i * 7 % 100, octave=oct + 3 % 4 + 3))
        m_list[2].add_note(N(i + 7 * i, (1, 4), velocity=i * 7 % 100, octave=oct + 2 % 4 + 3))
        m_list[3].add_note(N(i + 8 * i, (1, 6 + (i % 3)), velocity=i * 7 % 100, octave=oct + 1 % 4 + 3))
        m_list[4].add_note(N(i + 10 * i, (1, 4), velocity=i * 7 % 100, octave=oct + 4 % 4 + 3))

    for melody in m_list:
        melody.update_values()
    piece = P(m_list)
    piece.make_ready_to_play()
    piece.play(120)

    # notishift_input()


if __name__ == "__main__":
    main()
