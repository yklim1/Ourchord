def midicreate(notelist):
    #change_list=[8,5,6,'Rest',1,3]
    #tempo_list=[1/2,1/2,1/4,1/4,1/2,1/2]
#0  1  2  3  4  5  6  7  8  9  10  11
#C  C# D  D# E  F  F# G  G# A  A#  B
    NoteList = []
    print(notelist)
    for i in range(len(notelist)):
        #print(notelist[i][2],notelist[i][3],notelist[i][5])
        if(notelist[i][3]=='Rest'):
            chord = NoteSeq(Rest(notelist[i][2]))
        elif(notelist[i][5]==0):
            continue
        elif(notelist[i][5]==2):
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2]),Note(notelist[i+1][3],dur=notelist[i][2])])
        elif(notelist[i][5]==3):
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2]),Note(notelist[i+1][3],dur=notelist[i][2]),Note(notelist[i+2][3],dur=notelist[i][2])])
        elif(notelist[i][5]==4):
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2]),Note(notelist[i+1][3],dur=notelist[i][2]),Note(notelist[i+2][3],dur=notelist[i][2]),Note(notelist[i+3][3],dur=notelist[i][2])])
        else:
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2])])
        

        NoteList.append(chord)

        #else:
            #NoteList.append(Rest(notelist[i][2]))

    print(NoteList)
    #seq = NoteSeq(NoteList)
        
    #midi = Midi(number_tracks=2, tempo=90)
    #midi.seq_notes(NoteList, track=0)
    #midi.seq_notes(notes2, track=0)
    midi = Midi(1, tempo=60)
    midi.seq_chords(NoteList, track=0)
    midi.write(".vscode//demotest.mid")
