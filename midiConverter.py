from mido import MidiFile
from mido import bpm2tempo
from mido import tick2second

midiFile = MidiFile("TouchTheSky8bit.midi", clip = True)
name = "TouchTheSky"
SongFileHeader = '''#include "melodyClass.h" \n#include "melodyLibrary.h" \n#include "pitches.h \n\n// Generated Song File \n\n'''

notes = []
duration = []

track = midiFile.tracks[0]
print(track)

for msg in track:
    if msg.type == 'note_on':
        freq = (2**((msg.note-69)/12))*440 # midi number to frequencies
        notes.append(round(freq))
        duration.append(round(tick2second(msg.time, midiFile.ticks_per_beat, bpm2tempo(120))*(10**3))) # to milliseconds
        print(msg)

print(midiFile.ticks_per_beat)
print(len(notes))

outputString = "melody_t<" + str(len(notes)) + "> MelodyLibrary::" + name + " = { { {\n" 

for idx in range(len(notes)):
    if idx == len(notes) - 1:
        outputString += "{" + str(notes[idx]) + "," + str(duration[idx]) + "}\n} }, \ntrue \n };"
    else:
        outputString += "{" + str(notes[idx]) + "," + str(duration[idx]) + "},\n"

outputFile = open(name + ".cpp", "w")
outputFile.write(SongFileHeader)
outputFile.write(outputString)
outputFile.close()