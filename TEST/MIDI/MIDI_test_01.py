import pyknon
from __future__ import division
from fractions import Fraction

# integer notation
def mod12(n):
    return n % 12

# simple function to not integer
def note_name(number):
    notes = "C C# D D# E F F# G G# A A# B". split()
    return notes[mod12(number)]

# calculate the number that represents note
def accidentals(note_string):
    acc = len(note_string[1 : ])
    if "#" in note_string:
        return acc
    elif "b" in note_string:
        return -acc
    else:
        return 0

# C###
def name_to_number(note_string):
    notes = "C . D . E F . G. . A . B". split()
    name = note_string[0 : 1].upper()
    number = notes.index(name)
    acc = accidentals(note_string)
    return mod12(number + acc)

# note value - 1
def note_duraion(note_value, unity, tempo):
    return (60.0 * note_value) / (tempo * unity)

# note value - 2
def durations(notes_values, unity, tempo):
    return [note_duraion(nv, unity, tempo) for nv in notes_values]

# tempo - fraction
def dotted_duration(duration, dots):
    ratio = Fraction(1, 2)
    return duration * (1 - ratio ** (dots + 1)) / ratio

# semitones
def interval(x, y):
    return mod12(x - y)

# transposition - number to alpha
def transposition(notes, index):
    return [mod12(n + index) for n in notes]

# transposition - reverse
def retrograde(notes):
    return list(reversed(notes))

# rotate
def rotate(item, n = 1):
    modn = n % len(item)
    return item[modn : ] + item[0 : modn]
