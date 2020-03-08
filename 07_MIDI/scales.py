#!/usr/bin/env python

from math import factorial
from pyknon import simplemusic, pcset
from pyknon.music import NoteSeq, Note
from pyknon.genmidi import Midi


def numbers_to_noteseq(numbers):
    return NoteSeq([Note(n) for n in numbers])


def harmonize_all_scales():
    for forte, pc_set in pcset.PC_SETS.items():
        scale = NoteSeq([Note(n) for n in pc_set])
        scale.harmonize()


def harmonize_scale(forte):
    pitch_set = pcset.PC_SETS[forte]
    scale = numbers_to_noteseq(pitch_set)
    midi = Midi()
    t0 = midi.seq_notes(scale)
    t1 = midi.seq_chords(scale.harmonize(interval=3), time=t0 + 1)
    t2 = midi.seq_chords(scale.harmonize(interval=4), time=t1 + 1)
    midi.seq_chords(scale.harmonize(interval=5), time=t2 + 1)
    midi.write("midi/scales.midi")


def filter_sets(condition, all_sets=pcset.PC_SETS):
    sets = {}
    for forte, pc_set in all_sets.items():
        intervals = simplemusic.intervals(pc_set)
        size = len(pc_set)
        if condition(intervals, size):
            sets[forte] = pc_set
    return sets


def chord_combinations(n, k):
    return factorial(n) / (factorial(n - k) * factorial(k))



if __name__ == "__main__":
    harmonize_scale('7-21')
