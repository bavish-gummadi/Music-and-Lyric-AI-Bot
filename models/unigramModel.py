import random
from nGramModel import *

class UnigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the UnigramModel object)
        Effects:  this is the UnigramModel constructor, which is done
                  for you. It allows UnigramModel to access the data
                  in the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(UnigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        textData=self.prepData(text)  #might be wrong
        self.nGramCounts
        for line in textData:
            for x in range(2,len(line)):
                value=self.nGramCounts.get(line[x], 0)
                value=value+1
                self.nGramCounts[line[x]]=value




        pass

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        if(len(self.nGramCounts)!=0):
            return True

        else:
            return False
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNgGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts

        pass

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your test cases here
    text = [ ['the', 'quick', 'brown', 'fox', 'brown'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'brown' ]
    sentence2 = [ 'wrong' ]
    unigramModel = UnigramModel()
    unigramModel.trainModel(text)
    
    ##unigramModel1=UnigramModel()
    #unigramModel.trainModel(text)
    #unigramModel.trainingDataHasNGram(sentence)
    #unigramModel.trainingDataHasNGram(sentence2)
    #unigramModel1.trainingDataHasNGram(sentence)
    #unigramModel1.trainingDataHasNGram(sentence2)
    #unigramModel1.getCandidateDictionary(sentence)
    #unigramModel1.getCandidateDictionary(sentence2)
    #unigramModel.getCandidateDictionary(sentence)
    #unigramModel.getCandidateDictionary(sentence)
    print(unigramModel)
    print unigramModel.getNextToken(sentence)
