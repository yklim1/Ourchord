from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

# note1 = NoteSeq("D4 F#8 A Bb4")
note1 = NoteSeq("C9 D9 E5 E6")
midi = Midi(1, tempo = 90)
midi.seq_notes(note1, track = 0)
midi.write("demo5.mid")