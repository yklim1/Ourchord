#!/usr/bin/env python

from pyknon.music import Note, NoteSeq
from pyknon.genmidi import Midi


def josquin():
    main_theme = NoteSeq("file://josquin")
    theme1 = main_theme.stretch_dur(0.66666)
    theme2 = main_theme[0:24].stretch_dur(2).transp(Note("C"))
    theme3 = main_theme[0:50]

    midi = Midi(3, tempo=80)
    midi.seq_notes(theme1, track=0)
    midi.seq_notes(theme2, track=1)
    midi.seq_notes(theme3, track=2)
    midi.write("midi/josquin.mid")
