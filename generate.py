#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import tweepy
import random
import nltk
import StdOutListener
from pysynth import pysynth
from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import * 
from nltk.corpus import cmudict
pronDict = cmudict.entries()

# FIXME Add your team name
TEAM = 'BATT Productions'
BEATLESDIRS = ['the_beatles']
CASHDIRS=['Johnny_Cash']
DYLANLYRICSDIRS = ['Bob_Dylan']
QUEENDIRS = ['Queen']
SIMONDIRS =['Paul_Simon']
JACKSONDIRS=['Michael_Jackson']
KANYEDIRS=['Kanye_West']
EMINEMDIRS=['Eminem']
BEYDIRS=['Beyonce']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

###############################################################################
# Helper Functions
###############################################################################

def sentenceTooLong(desiredLength, currentLength):
    """
        Requires: nothing
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this sentence should
        be ended based on its length. This function has been done for
        you.
        """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength



def trainLyricModels(lyricDirs):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.

              Returns the list of trained models.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    global uniList
    uniList = []
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        uniList.append(lyrics)
        for model in models:
            model.trainModel(lyrics)
    return models

###############################################################################
# Core
###############################################################################

def trainMusicModels(musicDirs):
    """
    Requires: lyricDirs is a list of directories in data/midi/
    Modifies: nothing

    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    # call dataLoader.loadMusic for each directory in musicDirs
    for mdir in musicDirs:
        music=loadMusic(mdir)
        for model in models:
            model.trainModel(music)
    return models
    pass

def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  returns the best possible model that can be used for the
              current sentence based on the n-grams that the models know.
              (Remember that you wrote a function that checks if a model can
              be used to pick a word for a sentence!)
    """
    for gram in models:
        if gram.trainingDataHasNGram(sentence):
            return gram
    pass

def generateLyricalSentence(models, desiredLength, last_word = ''):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    # return a list of strings
    # loop until sentenceTooLong returns true or next token chose
    # adds a word
    models = models
    desiredLength = desiredLength
    results = ['^::^', '^:::^']
    sentence = selectNGramModel(models, ['^::^', '^:::^']).getNextToken(['^::^', '^:::^'])
    tagged = tag(results)
    while sentence !='$:::$':
        if sentenceTooLong(desiredLength, len(results)):
            break
        results.append(sentence)
        tagged = tag(results)
        if during(tagged):
            del results[-1]
            del tagged[-1]
        sentence = selectNGramModel(models, results).getNextToken(results)
    results.remove('^::^')
    results.remove('^:::^')
    k = get_Rhyme(last_word, uniList, pronDict)
    if k != None:
        results.append(k)
    del tagged[0]
    del tagged[0]
    results2 = after(tagged, results)
    empty = []
    if results2 == empty:
        results2 = generateLyricalSentence(models, desiredLength)
    return results2
    pass


def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateLyricalSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """

    results = ['^::^', '^:::^']
    sentence = selectNGramModel(models, ['^::^', '^:::^']).getNextNote(['^::^', '^:::^'], possiblePitches)

    while sentence != '$:::$':
        if sentenceTooLong(desiredLength, len(results)):
            break
        results.append(sentence)
        sentence = selectNGramModel(models, results).getNextNote(results, possiblePitches)
    results.remove('^::^')
    results.remove('^:::^')
    return results
    pass

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """

    verseOne = []
    for x in range(0, 6):
        verseOne.append(generateLyricalSentence(models, 10))
    verseTwo = []
    for x in range(0, 6):
        verseTwo.append(generateLyricalSentence(models, 10))
    chorus = []
    for x in range(0, 6):
        chorus.append(generateLyricalSentence(models, 10))
    printSongLyrics(verseOne, verseTwo, chorus)


def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator as following the details in the spec.
    """
    list = KEY_SIGNATURES.keys()
    desiredLength = 200
    value = random.choice(list)
    possiblePitches = KEY_SIGNATURES[value]
    tuplesList = generateMusicalSentence(models, desiredLength,possiblePitches)
    pysynth.make_wav(tuplesList, fn=songName)

    pass


###############################################################################
# Reach
###############################################################################
consumer_key = 'dkXRLqG8EgYC9GOmsR8kTqXV4'
consumer_secret = 'sjyfYIQxuSn6qAbzo5iLEaFLWPVHLiJOak73nx61JZZhumfrpE'
access_token = '938527466771177472-DeNwYIQJXnHxUF66aluqA9ZiCwMD0jc'
access_token_secret = 'wmgWdLB56LPU00RwFpGuUzfwImX9Rgj05HxsZ6UtqM5xI'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getPronunciation(in_word, entries):
    """
    Requires: in_word which is a string and entries which is a list from NLTK
    Modifies: nothing
    Effects: Searches entries for the correspoding pronounciation of in_word
    and returns the pronounciation. 
    """
    for word, pron in entries:
        if word == in_word:
            return pron
    pass

def check_rhymes(word1, word2, entries):
    """
    Requires: two strings and a list of entries from NLTK 
    Modifies: nothing
    Effects: Iterates through entries to find words that are pronounced similarly
    to word1. Any word with 2 or more sound matches is added to matches. The list
    matches is then searched for word2. If word1 is not found in entries for
    pronounciation, or word2 is not found in matches, this will return false.
    Otherwise, if word2 is found in matches, returns true. 
    """ 
    in_pron = getPronunciation(word1, entries)
    if in_pron is None:
        return False # word not in corpus
    matches = []
    for word, pron in entries:
        if word == word1:
            continue
        i=1 # reverse iterator
        n=0 # number of consecutive matching syllables
        while True:      
            if len(in_pron) < i or len(pron) < i:
                break
            elif pron[-i] <> in_pron[-i]:
                break
            else:
                i+=1
                n+=1
            if n>0:
                matches.append((word))
    for element in matches:
        if word2 == element:
            return True
    return False
    pass

def trainUnigramModels(lyricDirs):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance ofunigrams and trains themusing the text loaded
              from the data loader.
              Returns the list of trained unigram models.
    """
    models = [UnigramModel()]
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        for model in models:
            model.trainModel(lyrics)
    return models

def get_Rhyme(word1, wordList, entries):
    """
    Requires: A string, and a list of possible words to rhyme with,
    and a list of entries from NLTK 
    Modifies: nothing
    Effects: Iterates through entries to find words that are pronounced similarly
    to word1. Any word with 2 or more sound matches is added to matches. The list
    matches is then searched for word2. If word1 is not found in entries for
    pronounciation, or word2 is not found in matches, this will return false.
    Otherwise, if word2 is found in matches, returns true. 
    """ 
    in_pron = getPronunciation(word1, entries)
    random.shuffle(wordList)
    if in_pron is None:
        return None # word not in corpus
    matches = []
    for word, pron in entries:
        if word == word1:
            continue
        i=1 # reverse iterator
        n=0 # number of consecutive matching syllables
        while True:      
            if len(in_pron) < i or len(pron) < i:
                break
            elif pron[-i] <> in_pron[-i]:
                break
            else:
                i+=1
                n+=1
            if n>2:
                matches.append((word))
    for sentence in wordList:
        for lyric in sentence:
            for w in lyric:
                for element in matches:
                    if w == element:
                        return w
    return None
    pass

def after (tagged, results):
    """
    Requires: results is a list of strings
              tagged is a list of tuples that contains results's strings
              and their respective part of speech
    Modifies: nothing
    Effects:  returns results with edited grammar or empty if the sentence
              is too short
    """
    endWord=''
    begWord=''

    while results[-1] != endWord or results[0] != begWord:
        endWord = results[-1]
        begWord = results[0]
        if tagged[0][1][0:2] == 'CC':
            del results[0]
            del tagged[0]
        if tagged[-1][1][0:2] == 'CC':
            del results[-1]
            del tagged[-1]
        if tagged[-1][1][0:2] == 'IN':
            del results[-1]
            del tagged[-1]
        if tagged[-1][1][0:2] == 'TO':
            del results[-1]
            del tagged[-1]
        if tagged[-1][1][0:2] == 'DT':
            del results[-1]
            del tagged[-1]
        if tagged[-1][1][0:3] == 'PRP':
            del results[-1]
            del tagged[-1]
    for item in range(0,len(tagged)):
        if tagged[item][1][0:2] == 'NN':
            if len(results) > 3:
                return results

    for item in range(0,len(results)):
        del results[0]
    return results

    pass

def tag(results):
    """
    Requires: results is a list of strings
    Modifies: nothing
    Effects:  returns a tuple that contains results with each index's part
              of speech
    """
    tagged = nltk.pos_tag(results)
    tagged[0] = ('blank', 'FW')
    tagged[1] = ('blank', 'FW')
    return tagged
    pass

def during(tagged):
    """
    Requires: tagged is a list of tuples
    Modifies: nothing
    Effects:  returns true if the grammar rules are not broken
    """
    if tagged[-1][1][0:2] == 'CC' and tagged[-2][1][0:2] == 'CC':
        return True
    if tagged[-1][1][0:2] == 'TO' and tagged[-2][1][0:2] == 'TO':
        return True
    if tagged[-1][1][0:3] == 'PRP' and tagged[-2][1][0:3] == 'PRP':
        return True

    pass

def genTweetSentence(listWords):
    """
    Requires: listWords which is a list of strings
    Modifies: nothing
    Effects: Returns a the list of strings as one string sentence
    """
    tweet_sentence = ''
    for phrase in listWords:
        for word in phrase:
            tweet_sentence = tweet_sentence + word + ' '
        tweet_sentence = tweet_sentence + '\n'
    return tweet_sentence

def searchTweets(search, response, x):
    """
        Requires: something to search which is a keyboard inputted string
                  and what to respond which is from gentweetsentence
        Modifies: nothing
        Effects:  Searches for 'search' and the response is printed to the
                  twitter screens
        """
    print response

    twts = api.search(q=search)
    # list of specific strings we want to check for in Tweets
    for s in twts:
        if search.lower() in s.text.lower():
            sn = s.user.screen_name
            if x==1:
                m = "@%s" % (sn) + " Here's a Beatles inspired poem:\n\n" + response
            elif x==2:
                m = "@%s" % (sn) + " Here's a Bob Dylan inspired poem:\n\n" + response
            elif x==3:
                m = "@%s" % (sn) + " Here's a Johnny Cash inspired poem:\n\n" + response
            elif x==4:
                m = "@%s" % (sn) + " Here's a Queen inspired poem:\n\n" + response
            elif x==5:
                m = "@%s" % (sn) + " Here's a Michael Jackson inspired poem:\n\n" + response
            elif x==6:
                m = "@%s" % (sn) + " Here's a Eminem inspired poem:\n\n" + response
            elif x==7:
                m = "@%s" % (sn) + " Here's a Kanye West inspired poem:\n\n" + response
            elif x==8:
                m = "@%s" % (sn) + " Here's a Beyonce inspired poem:\n\n" + response
            elif x==9:
                m = "@%s" % (sn) + " Here's a Paul Simon inspired poem:\n\n" + response
            s = api.update_status(m, s.id)
            break

    pass
def runTweetGenerator(models, num):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls genTweetSentence and update_status to tweet a verse.
    """

    verseOne = []
    for x in range(0, 3):
        if x > 0:
            verseOne.append(generateLyricalSentence(models, 10, verseOne[x-1][-1]))
        else:
            verseOne.append(generateLyricalSentence(models, 12))
    searchPrompt= 'What should we search for? '
    search = raw_input(searchPrompt)
    response=genTweetSentence(verseOne)
    searchTweets(search, response, num)
    print "Your response(s) have been posted!"

def choiceOne():


    while True:
        try:
            userInput2 = int(raw_input(PROMPT2))
            if userInput2 ==1:
                runMaster(BEATLESDIRS,userInput2)
            elif userInput2 ==2:
                runMaster(DYLANLYRICSDIRS,userInput2)
            elif userInput2 ==3:
                runMaster(CASHDIRS,userInput2)
            elif userInput2 ==4:
                runMaster(QUEENDIRS,userInput2)
            elif userInput2 ==5:
                runMaster(JACKSONDIRS,userInput2)
            elif userInput2 ==6:
                runMaster(EMINEMDIRS,userInput2)
            elif userInput2 ==7:
                runMaster(KANYEDIRS,userInput2)
            elif userInput2 ==8:
                runMaster(BEYDIRS,userInput2)
            elif userInput2 ==9:
                runMaster(SIMONDIRS,userInput2)
            elif userInput2 == 10:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
        except ValueError:
            print("Please enter a number")


def runMaster(dirc, input):
    print('Starting program and loading data...')
    model = trainLyricModels(dirc)
    print('Data successfully loaded')
    runTweetGenerator(model, input)

PROMPT = """
(1) Run the TweetBot for Artist inspired poems
(2) Generate a song using data from Nintendo Gamecube
(3) Quit the music generator
> """

PROMPT2 = """
(1) Run the TweetBot for The Beatles
(2) Run the TweetBot for Bob Dylan
(3) Run the TweetBot for Johnny Cash
(4) Run the TweetBot for Queen
(5) Run the TweetBot for Michael Jackson
(6) Run the TweetBot for Eminem
(7) Run the TweetBot for Kanye West
(8) Run the TweetBot for Beyonce
(9) Run the TweetBot for Paul Simon
(10) Exit the TweetBot


> """
def main():
#list of specific strings we want to check for in Tweets

    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """
    


    print('Welcome to the ' + TEAM + 'Poetry and Music generator!')
    while True:
        try:
            userInput = int(raw_input(PROMPT))
            if userInput == 1:
                choiceOne()
            elif userInput == 2:
                print('Starting program and loading data...')
                musicModels = trainMusicModels(MUSICDIRS)
                print('Data successfully loaded')
                songName = raw_input('What would you like to name your song? ')
                runMusicGenerator(musicModels, WAVDIR + songName + '.wav') 
            elif userInput == 3:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")

if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
