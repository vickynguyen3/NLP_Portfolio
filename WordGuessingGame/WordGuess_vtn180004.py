# Vicky Nguyen, vtn180004
# CS 4395.001
# Word Guessing Game, Ch.5

import sys
import pathlib
import nltk

# function to preprocess raw text
def processTxt(txt_in):
    # a. tokenize lower-case raw text, reduce tokens to only those that are
    # alpha, not in the NLTK stopword list, and have length >5
    

    # b. lemmatize the tokens and use set() to make a list of unique lemmas
    lemmas = set()

    # c. do pos tagging on the unique lemmas and print the first 20 tagged
    tokens = nltk.word_tokenize(lemmas)
    tags = nltk.pos_tag(tokens)
    print(tags)


    # d. create a list of only those lemmas that are nouns

    # e. print number of tokens (from step a ) and number of nouns (step d)

    # f. return tokens (not unique tokens) from step a, and nouns from the function
    return


# guessing game function
def guessGame():
    # give user 5 points to start with; game ends when their total score is negative
    # or they guess '!' as a letter

    # randomly choose one of the 50 words in the top 50 list (see random
    # numbers notebook in the Xtras folder of the github)

    # output to console an "underscore space" for each letter in the word

    # ask the user for a letter

    # if the letter is in the word, print 'Right!', fill in all matching letter _ with the letter
    # and add 1 point to their score

    # if the letter is not in the word, subtract 1 from the score, print 'Sorry, guess again'

    # guessing for a word ends if the user guesses the word or has a negative score

    # keep a cumulative total score and end the game if it is negative (or the user entered '!') for a guess

    # right or wrong, give user feedback on their score for this word after each guess

    return


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
    txt_in = file.read()


# declare noun dictionary 
nounDict = {}

# call function to preprocess the raw text
# make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens list
processTxt(txt_in)

# sort dict by count and print the 50 most common words and their counts.
# save these words to a list bc they will be used in the guessing game

# calculate lexical diversity of the tokenized text

# output, formatted to 2 decimal places
