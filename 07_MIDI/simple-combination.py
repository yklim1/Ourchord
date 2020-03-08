#!/usr/bin/env python

from pyknon.simplemusic import inversion_startswith, transposition_startswith, retrograde, transposition
from pyknon.music import Note, NoteSeq
from pyknon.genmidi import Midi


motif = [0, 1, 7, 3]
a = inversion_startswith(motif, 11)
b = transposition_startswith(motif, 5)
c = retrograde(transposition_startswith(motif, 1))
notes = motif + a + b + c

note_list = NoteSeq([Note(x, dur=0.125) for x in notes])
midi = Midi(tempo=120)
midi.seq_notes(note_list)
midi.write("midi/simple-combination1.mid")
