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
import random
from collections import Counter

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
    print('\nFirst 20 Tagged:')
    for x in range(0, 20):
        print(tags[x])
     
    # create list of only lemmas that are nouns
    nouns = []

    # for loop over the tuple (tags)
    for lemma, pos in tags:
        if pos == 'NN':
            nouns.append(lemma)

    # print number of tokens 
    print('\nNumber of Tokens: ' + str(len(tok_txt)))
    # print number of nouns
    print('Number of Nouns: ' + str(len(nouns)))

    # return tokens (not unique tokens) from step a, and nouns from the function
    return tok_txt, nouns 

# helper method for guessing game
def match_guess(choice, guess_list, user_list):
    
    # find index where choice matches in guess_list
    for x in range(len(guess_list)):
        if choice == guess_list[x]:
            # with the indexes found, update user_list with letter
            user_list[x] = choice

    return user_list

# guessing game function
def guessGame(wordList):

    # give player 5 pts to start with
    total_pts = 5
    guessed_letters = []
    # randomly choose one of the 50 words in the top 50 list 
    guess_word = random.choice(wordList)

    # char list of the guess word
    guess_list = [*guess_word]
    # underscores
    user_list = [u for u in len(guess_word) * '_']
    
    # player plays as long as it's not a negative score or guess '!' as a letter
    while total_pts > -1:
        
        # output "underscore space" for each letter in word
        print(user_list)
        
        # player solved the word
        if guess_list == user_list:
            print('You solved it!\n')
            print('Current Score: ' + str(total_pts) + '\n')
            break

        # ask the user for a letter
        choice = input('Guess a Letter: ')

        # end game if player guess '!'
        if choice == '!':
            break
        # if player guessed right
        elif choice in guess_list:
            # check if letter has not been used already, repeats if player guess same letter
            if choice not in guessed_letters:
                # call function to fill in all matching letter _ with the letter
                user_list = match_guess(choice, guess_list, user_list)
                
                # add points to total score
                total_pts = total_pts + 1
                guessed_letters.append(choice)

                print('\nRight! Score is ' + str(total_pts)) 
        # player guessed wrong
        else:
            # subtract points to total score
            total_pts = total_pts - 1
            
            if total_pts < 0:
                break

            print('\nSorry, guess again. Score is ' + str(total_pts))
    # end of while loop
        
    if total_pts < 0 or choice == '!':
        print('-- Game Over --')

    # ask if player want to play guessing game again    
    ans = input('Do you want to play again? (y/n): ')
    
    if ans == 'y':
        print('\nGuess another word')
        # recurse back to play again
        return guessGame(wordList)
    else: 
        # print game over and quit game        
        print('Game Over, Quiting Game...')
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
print('Lexical Diversity: ' + str(round(lexDiv, 2)))

# call function to preprocess the raw text
tok_txt, nouns = processTxt(raw_txt)

# ----------- Dictionary -----------
# declare noun dictionary 
nounDict = {}
# declare freq number
nounFreq = FreqDist(tok_txt)

# make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens list
# sort dict by count 
wordDict = dict(sorted(nounFreq.items(), key=lambda item : item[1], reverse=True))

# save these words to a list bc they will be used in the guessing game
wordList = wordDict.keys()

# print the 50 most common words and their counts
print('\n50 Most Common Words and Their Counts:')

fiftyCount = wordDict.values()
print(Counter(tok_txt).most_common(50))

# ----------- Word Guessing Game -----------

print("\nLet's play a word guessing game!")

# call function to start word guessing game with the top 50 words
guessGame(list(wordList)[:50])
