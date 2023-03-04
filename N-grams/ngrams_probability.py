import nltk
import pickle
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

#
def calc_probability():
    # unigram 

    # bigram 

    # language

    # probablitily for the specific language

    return


# ----- main -----
try:
    # unpickle files

    # English
    with open("English_unigrams.pickle", "rb") as f:
        English_unigrams = pickle.load(f)
    with open("English_bigrams.pickle", "rb") as f:
        English_bigrams = pickle.load(f)

    # French
    with open("French_unigrams.pickle", "rb") as f:
        French_unigrams = pickle.load(f)
    with open("French_bigrams.pickle", "rb") as f:
        French_bigrams = pickle.load(f)

    # Italian
    with open("Italian_unigrams.pickle", "rb") as f:
        Italian_unigrams = pickle.load(f)
    with open("Italian_bigrams.pickle", "rb") as f:
        Italian_bigrams = pickle.load(f)
except:
    print('Error: Problem with loading in the pickled files')
else:
    try:
        # get the test texts
        #with open()
    except:
        print('Could')