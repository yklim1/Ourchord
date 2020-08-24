import pyknon
from __future__ import division
from fractions import Fraction

from pyknon.simplemusic import get_quality


def mod12(n):
    return n % 12

def note_name(number):
    notes = "C C# D D# E F F# G G# A A# B".split()
    return notes[mod12(number)]

def accidentals(note_string):
    acc = len(note_string[1 : ])
    if "#" in note_string:
        return acc
    elif "b" in note_string:
        return -acc
    else:
        return 0

def name_to_number(note_string):
    notes = "C . D . E F . G. . A . B". split()
    name = note_string[0 : 1].upper()
    number = notes.index(name)
    acc = accidentals(note_string)
    return mod12(number + acc)

def interval(x, y):
    return mod12(x - y)

def name_to_diatonic(note_string):
    notes = "C D E F G A B".split()
    name = note_string[0 : 1].upper()
    return notes.index(name)

def interval_name(note1, note2):
    quantities = ["Unison", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
    n1, n2 = name_to_number(note1), name_to_number(note2)
    d1, d2 = name_to_diatonic(note1), name_to_diatonic(note2)
    chromatic_interval = interval(n1, n2)
    diatonic_interval = (d2 - d1) % 7
    quantity_name = quantities[diatonic_interval]
    quality_name = get_quality(diatonic_interval, chromatic_interval)
    return "%s %s" % (quality_name, quantity_name)
