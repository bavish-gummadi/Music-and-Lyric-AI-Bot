#!/usr/bin/env python
import os
import re
import string

def loadLyrics(dirName):
    """
    Loads the lyrics files from the directory specified by dirName,
    if that directory exists. For each line in each file,
    cleans that line by removing punctuation and extraneous
    whitespaces, and lowercasing all words in the line.
    """
    lyricsDir = os.path.dirname(os.path.abspath(__file__)) + "/lyrics/"
    artistDir = os.path.join(lyricsDir, dirName) + "/"

    if not os.path.isdir(artistDir):
        print "No artist named", artistDir, "in directory", lyricsDir
        return None

    lyrics = []

    songs = os.listdir(artistDir)
    for song in songs:
        with open(artistDir + song, 'r') as songFile:
            songLines = songFile.readlines()

        # clean each line in each song and add if not empty
        for line in songLines:
            line = line.translate(None, string.punctuation)
            line = line.lower().strip()
            if line:
                lyrics.append(line.split())
    return lyrics

def loadMusic(dirName):
    """
    Loads the midi files to the specified dirName directory by
    extracting data out of those midi .txt files and converting that
    data into PySynth tuple format.
    """
    midiDir = os.path.dirname(os.path.abspath(__file__)) + "/midi/"
    platformDir = os.path.join(midiDir, dirName) + "/"

    if not os.path.isdir(platformDir):
        print "No platform named", platformDir, "in directory", midiDir
        return None

    midiFiles = os.listdir(platformDir)
    midiFiles = [platformDir + "/" + midiFile for midiFile in midiFiles]

    songs = []

    for midiFile in midiFiles:
        with open(midiFile, "r") as f:
            lines = f.readlines()

        song = []
        for line in lines:
            line = line.split()

            # extract pitch and duration from .txt song data, convert
            # those values to pysynth format, and add the
            # (pitch, duration) tuple to the song list
            if "TR" in line and line[line.index("TR") + 1] == "1" \
                    and "NT" in line:
                noteIndex = line.index("NT")
                pitch = line[noteIndex + 1]
                pitch = formatPitch(pitch)

                duration = line[noteIndex + 2]
                duration = formatDuration(duration)

                pysynthTuple = (pitch, duration)
                song.append(pysynthTuple)

        if song:
            songs.append(song)
    return songs

def formatPitch(asciiPitch):
    """
    Converts from the ASCII representation of a note's pitch to the
    PySynth representation of a note's pitch, returning the
    converted string.
    """
    pitch = asciiPitch.lower()

    # get octave value relative to 4
    octave = 4
    if "'" in pitch:
        numApostrophes = pitch.count("'")
        octave += numApostrophes
        if octave >= 8:
            octave = 7
        pitch = pitch.replace("'", "")
    elif "-" in pitch:
        numDashes = pitch.count("-")
        octave -= numDashes
        if octave <= 0:
            octave = 1
        pitch = pitch.replace("-", "")

    # i don't think pysynth likes e# or b#
    if pitch == "e#":
        pitch = "f"
    elif pitch == "b#":
        pitch = "c"

    # these shouldn't be a problem - test these
    if pitch.count("#") > 1:
        pitch = pitch[0] + "#"
    elif pitch.count("b") > 2:
        pitch = pitch[0] + "b"

    pitch += str(octave)
    return pitch

def formatDuration(asciiDuration):
    """
    Converts from the ASCII representation of a note's duration to the
    PySynth representation of a note's duration, as described in
    the spec. Returns the integer representing the duration.
    """
    duration = re.split("[+ /]", asciiDuration)

    if len(duration) == 1:
        duration = float(duration[0])
    elif len(duration) == 2:
        nominator = float(duration[0])
        denominator = float(duration[1])
        try:
            duration = nominator / denominator
        except ZeroDivisionError:
            duration = nominator
    elif len(duration) == 3:
        wholeNumber = float(duration[0])
        nominator = float(duration[1])
        denominator = float(duration[2])
        try:
            duration = wholeNumber + nominator / denominator
        except ZeroDivisionError:
            duration = wholeNumber
    else: # should never get here
        duration = 1

    if duration < 0.5:
        duration = 16
    elif duration >= 0.5 and duration < .75:
        duration = -8
    elif duration >= 0.75 and duration < 1:
        duration = 8
    elif duration >= 1 and duration < 1.5:
        duration = 4
    elif duration >= 1.5 and duration < 2:
        duration = -4
    elif duration >= 2 and duration < 3:
        duration = 2
    elif duration >= 3 and duration < 4:
        duration = -2
    else:
        duration = 1

    return duration

if __name__ == "__main__":
    lyrics = loadLyrics('the_beatles')
    for line in lyrics:
        print(line)
