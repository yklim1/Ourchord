from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest

first_note=Note("A...")

def key_number(n):
    return n.octave*12 + n.value - first_note.value

def note_from_key_number(k):
    return Note(k-51)

def intervals(notes):
    interval = []
    for n in range(len(notes)-1):
        interval.append(notes[n+1]-notes[n])
    return interval

piano_notes=map(note_from_key_number, range(88))
midi = Midi(1, tempo=80)
midi.seq_notes(piano_notes, track=0)
midi.write("piano_keys.mid")

middle_c=Note("C,")
note_nums=map(key_number, piano_notes)
print ("All piano notes:", note_nums)
print ("Middle C key number:", key_number(middle_c))

print ("C major (staring with middle C):", map(key_number, NoteSeq("C, D E F G A B")))
print ("C major:", map(key_number, C_major))
print ("Intervals for C major:", intervals(map(key_number, C_major)))
print ("A minor:", map(key_number, A_minor))
print ("Intervals A minor:", intervals(map(key_number, A_minor)))

####### Last we'll generate some chords in a major and minor keys.

def major_chord(root):
    root_key_num = key_number(root)
    return map(note_from_key_number, [root_key_num, root_key_num+4, root_key_num+7])

def minor_chord(root):
    root_key_num = key_number(root)
    return map(note_from_key_number, [root_key_num, root_key_num+3, root_key_num+7])

def dim_chord(root):
    root_key_num = key_number(root)
    return map(note_from_key_number, [root_key_num, root_key_num+3, root_key_num+6])

# Chord qualities: M m m M M m d (M)
major_chord_progression = [major_chord, minor_chord, minor_chord, major_chord, \
                           major_chord, minor_chord, dim_chord]

# Chord qualities: m d M m m M M (m)
minor_chord_progression = [minor_chord, dim_chord, major_chord, minor_chord, \
                           minor_chord, major_chord, major_chord]

####### Generate C major chords ###
C_maj_chords = []
for i in range(len(major_chord_progression)):
    C_maj_chords.append(major_chord_progression[i](C_major[i]))

# Throw a "mistake" in there to hear the difference
C_maj_chords.append([Note("C"), Note("F#"), Note("Bb")])

print ("C major chords:", C_maj_chords)

midi = Midi(1, tempo=80)
midi.seq_chords(map(NoteSeq, C_maj_chords))
midi.write("c_major_chords.mid")

####### Generate G minor chords ###
G_minor = NoteSeq("G, A Bb C' D Eb F")
G_min_chords = []
for i in range(len(minor_chord_progression)):
    G_min_chords.append(minor_chord_progression[i](G_minor[i]))
print ("G minor chords:", G_min_chords)

midi = Midi(1, tempo=80)
midi.seq_chords(map(NoteSeq, G_min_chords))
midi.write("g_minor_chords.mid")