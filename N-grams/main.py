# mdc190005, Meinhard Capucao
# vtn180004, Vicky Nguyen
# 3.04.23
# Tnis program finds the unigrams and bigrams of text files for English, French, and Italian.
# then, it pickles them into dictionaries.


import pickle
from nltk.util import ngrams
from nltk import word_tokenize

# Reads a file, with specified filename. Removes all newspace
def fileReader(filename):
    with open(filename, encoding="utf-8") as file:  # opens file name with proper encoding to read other langauges
        text = file.read().replace('\n', ' ')
    ### print(text)

    # Splits text into tokens
    tokens = text.split()

    # Creates a unigram list
    unigrams = list(ngrams(tokens, 1))
    ### print("Unigrams List length: ", len(unigrams))
    ### print("Unigrams Unique List length: ", len(set(unigrams)))

    # Creates a bigram list
    bigrams = list(ngrams(tokens, 2))

    ### print("Bigrams List length: ", len(bigrams))
    ### print("Bigrams Unique List length: ", len(set(bigrams)))

    # Creating dictionaries
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    ## print(unigram_dict)
    ## print(bigram_dict)
    return unigram_dict, bigram_dict

# Creates a unigram dictionary and a bigram dictionary for English, then pickles them.
unigram_dict1, bigram_dict1 = fileReader("LangId.train.English")
with open("English_unigrams.pickle", "wb") as f:
    pickle.dump(unigram_dict1, f)
with open("English_bigrams.pickle", "wb") as f:
    pickle.dump(bigram_dict1, f)

# Creates a unigram dictionary and a bigram dictionary for France, then pickles them
unigram_dict2, bigram_dict2 = fileReader("LangId.train.French")
with open("French_unigrams.pickle", "wb") as f:
    pickle.dump(unigram_dict2, f)
with open("French_bigrams.pickle", "wb") as f:
    pickle.dump(bigram_dict2, f)

# Creates a unigram dictionary and a bigram dictionary for Italian, then pickles them
unigram_dict3, bigram_dict3 = fileReader("LangId.train.Italian")
with open("Italian_unigrams.pickle", "wb") as f:
    pickle.dump(unigram_dict3, f)
with open("Italian_bigrams.pickle", "wb") as f:
    pickle.dump(bigram_dict3, f)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
