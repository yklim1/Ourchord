#!/usr/bin/env python

from pyknon.music import Note, NoteSeq
from pyknon.genmidi import Midi


def abstraction():
    a = NoteSeq("C4. Eb8")
    a1 = a.transp(5).stretch_dur(0.5)
    a2 = a.inv("Db''")
    a3 = a1.inv(8)

    A = a + a1 + a2 + a3
    A2 = A.transp(2)
    B = a1.transp(8) + a1.transp("Eb''")

    c = NoteSeq([Note(x.value, dur=0.125) for x in a + a1])
    C = (c.inv("Ab''") +
         c.inv(10) +
         c.stretch_interval(2).transp(2) +
         c.inv("G''") +
         c.inv("E''").stretch_interval(1) +
         c.inv("A").stretch_interval(1)
         )
    
    a4 = a.stretch_dur(2).inv(6)
    
    Part1 = A + NoteSeq("C2") + A2 + B
    Part2 = C + a4

    midi = Midi(1, tempo=90)
    midi.seq_notes(Part1 + Part2, track=0)
    midi.write("midi/abstraction.mid")

    
if __name__ == "__main__":
    abstraction()
