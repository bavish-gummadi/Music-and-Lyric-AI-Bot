import random
from nGramModel import *

class TrigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  this is the TrigramModel constructor, which is done
                  for you. It allows TrigramModel to access the data
                  from the NGramModel class.
        """
        super(TrigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        textData = self.prepData(text)
        self.nGramCounts = {}
        sub_diction = {}
        for phrase in textData:
            for i in range(0, len(phrase) - 2):
                if self.nGramCounts.get(phrase[i], 0) == 0:
                    self.nGramCounts[phrase[i]] = {}
                if self.nGramCounts[phrase[i]].get(phrase[i + 1], 0) == 0:
                    self.nGramCounts[phrase[i]][phrase[i + 1]] = {}
                a = self.nGramCounts[phrase[i]][phrase[i + 1]].get(phrase[i + 2], 0) + 1
                b = phrase[i + 1]
                c = phrase[i + 2]
                self.nGramCounts[phrase[i]][b].update({c: a})
        pass

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        word1 = sentence[len(sentence)-2]
        word2 = sentence[len(sentence)-1]
        if word1 in self.nGramCounts:
            if word2 in self.nGramCounts[word1]:
                return True
        return False
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """
        word1=sentence[len(sentence)-2]
        word2=sentence[len(sentence)-1]
        bigDict=self.nGramCounts.get(word1,0)
        realDict=bigDict.get(word2,0)
        return realDict
        pass


###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your tests here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'the', 'quick', 'brown' ]
    trigramModel = TrigramModel()
    trigramModel.trainModel(text)
    print trigramModel.trainingDataHasNGram(sentence)
    print(trigramModel)
    print trigramModel.getCandidateDictionary(sentence)



