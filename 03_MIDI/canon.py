#!/usr/bin/env python

from pyknon.music import Note, NoteSeq
from pyknon.genmidi import Midi


def canon():
    theme1 = NoteSeq("file://canon-quaerendo-invenietis")
    part1 = theme1 + theme1[2:] + theme1[2:11]
    part2 = theme1 + theme1[2:] + theme1[2:4]

    voice1 = part1
    voice2 = part2.inversion_startswith(Note(2, 4))

    midi = Midi(2, tempo=150)
    midi.seq_notes(voice1, time=3, track=0)
    midi.seq_notes(voice2, time=13, track=1)
    midi.write("midi/canon.mid")


def crab_canon():
    theme2 = NoteSeq("file://canon-crab")
    rev_theme = theme2.transposition(-12).retrograde()

    midi = Midi(2, tempo=120)
    midi.seq_notes(theme2)
    midi.seq_notes(rev_theme, track=1)
    midi.write("midi/canon-crab.mid")


if __name__ == "__main__":
    canon()
    crab_canon()
