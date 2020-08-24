#!/usr/bin/env python

from __future__ import division
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note


def demo():
    notes1 = NoteSeq("C C# D D# E F F# G G# A A# B")
    #notes2 = NoteSeq([Note(2, dur=1/4), Note(6, dur=1/8),
                    # Note(9, dur=1/8), Note(10, dur=1/4)])
    midi = Midi(number_tracks=2, tempo=90)
    midi.seq_notes(notes1, track=0)
    #midi.seq_notes(notes2, track=1)
    midi.write("/Users/zjisuoo/Documents/학교/OurChord/CODE/03_MIDI/demo.mid")


if __name__ == "__main__":
    demo()
