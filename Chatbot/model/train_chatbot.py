# Vicky Nguyen, vtn180004
# CS 4395.001
# Chatbot Project - Model Training

import numpy as np
import random
import pickle
import sklearn
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
stopwords = stopwords - set(['no', 'not', 'can', 'are', 'do', 'okay', 'like', 'know', 'am', 'who', 'want'])

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

# intents patterns
for i in intents['intents']:
    for pattern in i['patterns']:
        
        print(f'intent working on: {i["tag"]}')
        print(f'pattern working on: {pattern}')
        
        # tokenize each word
        pw = word_tokenize(pattern)
        
        # add to our words list
        words.extend(pw)

        # add to documents in our corpus
        documents.append((pw, i['tag']))

        # add to our classes list
        if i['tag'] not in classes:
            classes.append(i['tag'])

# stem and lower each word
stemmer = LancasterStemmer()
words = [stemmer.stem(pw.lower()) for pw in words if pw not in ignore_punct and pw not in stopwords]

# remove duplicates
words = sorted(set(words))
classes = sorted(set(classes))

# checking to see if everything is working
print(f'NUMBER OF DOCUMENTS: {len(documents)}')
print(f'NUMBER OF CLASSES: {len(classes)}', classes)
print(f'UNIQUE LEMMAS: {len(words)}', words)

# training data variables
training = []
training_output = []

# create an empty array for output
empty_arr = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    word_bag = []
    pattern_words = doc[0]

    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words if word not in list(stopwords)]

    for word in words:
        if word in pattern_words:
            word_bag.append(1)
        else:
            word_bag.append(0)

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

# --------------------------------- MODEL TRAINING ---------------------------------
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

# create model
neural_model = MLPClassifier(hidden_layer_sizes=(10, 8), max_iter=10000)
neural_model.fit(train_x, train_y)

# save model
pickle.dump(neural_model, open('neural_model.pkl', 'wb'))

# save all of our data structures
pickle.dump({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open('training_data.pkl', 'wb'))

# --------------------------------- 

def clean_up_sentence(sentence):

    # tokenize pattern
    sentence_words = word_tokenize(sentence)

    # stem each word
    stemmer = LancasterStemmer()
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words if word.isalpha() and word not in stopwords]

    return sentence_words

def bag_of_words(sentence, words):
    # clean sentence
    sentence_words = clean_up_sentence(sentence)

    # bag of words
    bag = [0]*len(words)

    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
                
    return(np.array(bag))

# predict the intent using a bag of words, returns descending list of probable responses
def classify(sentence):
    print(f'sentence: {sentence}')
    ERR_MARGIN = 0.25

    # generate probabilities from the model
    model_results = neural_model.predict_proba([bag_of_words(sentence, words)])[0]
    # filter out predictions below a threshold/margin
    model_results = [[i, r] for i, r in enumerate(model_results) if r > ERR_MARGIN]
    
    '''
    for res in model_results:
        print(f'prob: {res[1]}')
        print(f'class: {classes[res[0]]}')
    '''
    # sort by strength of probability and reverse it to descending order so most probable is first
    model_results.sort(key = lambda x: x[1], reverse = True)

    return_list = []

    for r in model_results:
        return_list.append((classes[r[0]], r[1]))
    print(f'return list: {return_list}')

    return return_list

debug = True
if (debug):
    classify('hi')
    classify('i back')
    classify('who are you')
    classify('what can you do')
    classify('thanks')
    classify('bye')
    classify('what do i dislike')
    classify('what do i like')
    classify('uhm')
    classify('not really')
    classify('i want to learn')
    classify('what do i hate?')
    #classify('i like the starry night')

    while True:
        user_input = input('>>: ')
        classify(user_input)
