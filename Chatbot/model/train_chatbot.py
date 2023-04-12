# Vicky Nguyen, vtn180004
# CS 4395.001
# Chatbot Project - Model Training
# Path: Chatbot\model\train_chatbot.py

import numpy as np
import random
import pickle
import sklearn
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
stopwords = stopwords - set(['no', 'not'])

# chatbot intents file
import json
with open('../intents.json') as json_data:
    intents = json.load(json_data)

# holds all the words that are derived from patterns (lemmatized)
words = []
classes = []
# corpus of words under specific intents
documents = []
# list of ignored punctuation
ignore_punct = ['?', '.', ',', '!']

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word
        pw = word_tokenize(pattern)
        
        # add to our words list
        words.extend(pw)

        # add to documents in our corpus
        documents.append((pw, intent['tag']))

        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatize and lower each word
stemmer = LancasterStemmer()
words = [stemmer.stem(pw.lower()) for pw in words if pw not in ignore_punct and pw not in stopwords]

# remove duplicates
words = sorted(set(words))
classes = sorted(set(classes))

# training data variables
training = []
training_output = []

# create an empty array for output
empty_arr = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize bag of words
    word_bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]

    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words if word not in list(stopwords)]

    # create bag of words array w/ 1, if word match found in current pattern
    for word in words:
        if word in pattern_words:
            word_bag.append(1)
        else:
            word_bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(empty_arr)
    output_row[classes.index(doc[1])] = 1

    # append to training data
    training.append([word_bag, output_row])

# shuffle features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])

from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

# create model
neural_model = MLPClassifier(hidden_layer_sizes=(10, 8), max_iter=10000)
neural_model.fit(train_x, train_y)

# save model
pickle.dump(neural_model, open('neural_model.pkl', 'wb'))

# save all of our data structures
pickle.dump({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open('training_data.pkl', 'wb'))

