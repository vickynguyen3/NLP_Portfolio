# mdc190005, Meinhard Capucao
# vtn180004, Vicky Nguyen
# 3.04.23
# Tnis program reads in pickled dictionaries. It then reads in a test file of different languages, then
# calculates a probability for the languages English, Italian, and French line by line. It relays the highest
# probability percentage language for each of the lines, then gives an accuracy score. Calculations are
# based on a laplace score.
# It also tells which lines had a wrong prediction.

import pickle
import math
from nltk.util import ngrams
from nltk import word_tokenize
from nltk import sent_tokenize
import nltk

# Opening english dictionaries
with open("English_unigrams.pickle", "rb") as f:
    English_unigrams = pickle.load(f)   # Unpickles English dictionary, unpickles it to a file called English_unigrams
with open("English_bigrams.pickle", "rb") as f:
    English_bigrams = pickle.load(f)    # Unpickles English dictionary, unpickles it to a file called English_bigrams

# Opening french dictionaries
with open("French_unigrams.pickle", "rb") as f:
    French_unigrams = pickle.load(f)    # Unpickles French dictionary, unpickles it to a file called French_unigrams
with open("French_bigrams.pickle", "rb") as f:
    French_bigrams = pickle.load(f)     # Unpickles French dictionary, unpickles it to a file called French_bigrams

# Opening italian dictionaries
with open("Italian_unigrams.pickle", "rb") as f:
    Italian_unigrams = pickle.load(f)    # Unpickles Italian dictionary, unpickles it to a file called Italian_unigrams
with open("Italian_bigrams.pickle", "rb") as f:
    Italian_bigrams = pickle.load(f)    # Unpickles Italian dictionary, unpickles it to a file called Italian_bigrams

# Similar filereader function to main, but instead returns a text file. Encoding utf-8 ensures it can read
# Italian and French
def fileReader(filename):
    with open(filename, encoding="utf-8") as file:  # opens file name with proper encoding to read other langauges
        text = file.read()
        return text

# Imports LangId.test, the test file and splits it into a list of lines in a variable named "test_sentences"
test_text = fileReader("LangId.test")
test_sentences = test_text.splitlines()

# print(test_text)
# print(test_sentences)

# sets line number to 1

line_number = 1;

# opens a file called predictions.txt in a different mode than append, the closes it. this flushes the file and
# makes sure there isn't anything there
open("predictions.txt", "w").close()
output_list = []            # makes an empty list that will represent the different outputs.

# iterates through the test file for languages to be predicted, line by line.
for line in test_sentences:
    # creates an output file to put predictions in the format '{Line number} {Language predicted}
    output_file = open("predictions.txt", "a")
    unigrams_test = word_tokenize(line)
    bigrams_test = list(ngrams(unigrams_test, 2))

    # creates a text file for these three languages just in case we need them
    english = fileReader("LangId.train.English")
    french = fileReader("LangId.train.French")
    italian = fileReader("LangId.train.Italian")

    # Sets the V value for each language, the number of keys (unique tokens) for each unigram
    englishV = len(English_unigrams.keys())
    frenchV = len(French_unigrams.keys())
    italianV = len(Italian_unigrams.keys())

    # Sets the laplance value for each language to 1 at the beginning of each line read from the test file
    english_laplace = 1
    italian_laplace = 1
    french_laplace = 1

    # Iterates through each individual bigram in the test file line
    for bigram in bigrams_test:
        # Find each languages n and d values, calculactions used to find the overall laplance
        english_n = English_bigrams[bigram] if bigram in English_bigrams else 0
        english_d = English_unigrams[bigram[0]] if bigram[0] in English_unigrams else 0
        italian_n = Italian_bigrams[bigram] if bigram in Italian_bigrams else 0
        italian_d = Italian_unigrams[bigram[0]] if bigram[0] in Italian_unigrams else 0
        french_n = French_bigrams[bigram] if bigram in French_bigrams else 0
        french_d = French_unigrams[bigram[0]] if bigram[0] in French_unigrams else 0
        english_laplace = english_laplace * ((english_n + 1) / (english_d + englishV))
        italian_laplace = italian_laplace * ((italian_n + 1) / (italian_d + italianV))
        french_laplace = french_laplace * ((french_n + 1) / (french_d + frenchV))

    # print("English probability with laplace smoothing is", english_laplace)
    # print("Italian probability with laplace smoothing is", italian_laplace)
    # print("French probability with laplace smoothing is", french_laplace)

    # Finds the highest probability out of the three
    max_prob = max(english_laplace, italian_laplace, french_laplace)

    # If max prob is english, put it to the output file, then append it to the output list for use later
    if max_prob == english_laplace:
        highest_laplace = english_laplace
        output_file.write(str(line_number) + " English\n")
        output_list.append(str(line_number) + " English")
        print("We are at line number: ", line_number, ", English has the highest probability")
    # If max prob is italian, put it to the output file, then append it to the output list for use later
    elif max_prob == italian_laplace:
        highest_laplace = italian_laplace
        output_file.write(str(line_number) + " Italian\n")
        output_list.append(str(line_number) + " Italian")
        print("We are at line number: ", line_number, ", Italian has the highest probability")
    # If max prob is french, put it to the output file, then append it to the output list for use later
    else:
        highest_laplace = french_laplace
        output_file.write(str(line_number) + " French\n")
        output_list.append(str(line_number) + " French")
        print("We are at line number: ", line_number, ", French has the highest probability")
    line_number += 1

#Opens the solution file, then puts all the solutions into a list of strings that represent a line each
solution_file = fileReader("LangId.sol")
solution_list = solution_file.splitlines()

# Sets total_lines to the number of solutions, which corresponds to predictions made
total_correct = 0
wrong_lines = []
total_lines = len(solution_list)

# Iterates through each line and checks if prediction correct. If it is, add to the total.
# If prediction is wrong, update the wrong_lines list
for line in range(total_lines):
    if str(solution_list[line]) == str(output_list[line]):
        total_correct += 1
    else:
        wrong_lines.append(output_list[line])

# Prints accuracy
print("\nAccuracy: ", total_correct/total_lines, '\n')

# Loops through all incorrect predictions, the prints them. Also prints the line number of the incorrect guess
# and what it should've been instead
for line in wrong_lines:
    line_num, predicted_language = line.split()
    actual_language = ''
    for solution in solution_list:
        # If the line number matches for the solution, splits up the language so the correct one can be relayed
        if int(solution.split()[0]) == int(line_num):
            actual_language = solution.split()[1]
            break
    print("Line {} was wrong. {} was guessed, but in reality, it was {}.".format(
        line_num, predicted_language, actual_language))



