# Vicky Nguyen, vtn180004
# CS 4395.001
# Word Guessing Game, Ch.5

import sys
import pathlib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import math
import random

# function to preprocess raw text
def processTxt(raw_txt):

    # tokenize lower-case raw text
    tok_txt = [t.lower() for t in raw_txt]

    # make it only the words (alpha), not in NLTK stopword list, and len >5
    tok_txt = [t for t in tok_txt if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    # lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(t) for t in tok_txt]

    # set() to make list of unique lemmas
    lemmaList = list(set(lemmas))

    # do pos tagging on the unique lemmas
    tags = nltk.pos_tag(lemmaList)

    # print first 20 tagged
    print('First 20 Tagged:\n')
    for x in range(0, 20):
        print(tags[x])
     
    # create list of only lemmas that are nouns
    nouns = []

    # for loop over the tuple (tags)
    for lemma, pos in tags:
        if pos == 'NN':
            nouns.append(lemma)

    # print number of tokens 
    print('Number of Tokens: ' + str(len(tok_txt)))
    # print number of nouns
    print('Number of Nouns: ' + str(len(nouns)))

    # return tokens (not unique tokens) from step a, and nouns from the function
    return tok_txt, nouns 


# guessing game function
def guessGame(wordList):

    # give user 5 points to start with
    total_pts = 5

    print("Let's play a word guessing game!")
    # player plays as long as it's not a negative total score or guess '!' as a letter
    while total_pts >= 0 or choice is not '!':
        # top 50 words
        wordList = wordList[0:50]
        
        # randomly choose one of the 50 words in the top 50 list 
        guess_word = random.choice(wordList)

        # output to console an "underscore space" for each letter in the word
        guess_list = [*guess_word]
        user_list = [u for u in len(guess_word) * '_']

        print(user_list)

        # ask the user for a letter
        choice = input('Guess a Letter: ')

        # if the letter is in the word, print 'Right!', fill in all matching letter _ with the letter
        # and add 1 point to their score

        # if the letter is not in the word, subtract 1 from the score, print 'Sorry, guess again'

        # guessing for a word ends if the user guesses the word or has a negative score

        # keep a cumulative total score and end the game if it is negative (or the user entered '!') for a guess

        # right or wrong, give user feedback on their score for this word after each guess
    
    # print game over and quit game        
    print('-- Game Over --')
    quit()        


# ---------------- main ----------------
if __name__ == '__main__':

    # check if there's no sysarg
    if len(sys.argv) < 2:
        # print error msg and quit program
        print('Please enter a file name as a system argument')
        quit()

# user specifies relative path in a sysarg
rel_path = sys.argv[1]

# read input file and close the file
with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as file:
    raw_txt = word_tokenize(file.read())

# calculate lexical diversity of tokenized text
# number of unique tokens / by the total number of tokens
lexDiv = len(set(raw_txt)) / len(raw_txt)
# output, formatted to 2 decimal places
print('Lexical Diversity: ' + round(lexDiv, 2))

# call function to preprocess the raw text
tok_txt, nouns = processTxt(raw_txt)

# ----------- Dictionary -----------
# declare noun dictionary 
nounDict = {}
# declare freq number
nounFreq = FreqDist(tok_txt)

# make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens list
print('Dictionary:')
print(nounFreq)

# sort dict by count 
wordDict = dict(sorted(nounFreq.items(), key=lambda item : item[1], reverse=True))

# save these words to a list bc they will be used in the guessing game
wordList = wordDict.keys()
wordCount = wordDict.values()

# print the 50 most common words and their counts
print('50 Most Common Words and Their Counts:\n')
for x in range(0, 50):
    print(wordList[x] + ', Count: ' + wordCount[x])

# ----------- Word Guessing Game -----------

# call function to start word guessing game
guessGame(wordList)