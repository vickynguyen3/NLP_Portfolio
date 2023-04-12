# Vicky Nguyen, vtn180004
# CS 4395.001
# Chatbot Project

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np
import random
import json
import pickle
import sklearn
from sklearn.neural_network import MLPClassifier
import os

stopwords = set(stopwords.words('english'))
stopwords = stopwords - set(['no', 'not', 'nor', 'don', 'don\'t', 'ain', 'aren', 'aren\'t', 'couldn', 'couldn\'t', 'didn', 'didn\'t', 'doesn', 'doesn\'t', 'hadn', 'hadn\'t', 'hasn', 'hasn\'t', 'haven', 'haven\'t', 'isn', 'isn\'t', 'mightn', 'mightn\'t', 'mustn', 'mustn\'t', 'needn', 'needn\'t', 'shan', 'shan\'t', 'shouldn', 'shouldn\'t', 'wasn', 'wasn\'t', 'weren', 'weren\'t', 'won', 'won\'t', 'wouldn', 'wouldn\'t'])

userName = ''
context = ['']
bye = False
lemmatizer = WordNetLemmatizer()

# dictionary 
# {word: sentences that contain the word}
knowledge_base = pickle.load(open('knowledge_base.pkl', 'rb'))

# lemmatize words in knowledge base
knowledge_terms = knowledge_base.keys()

print(knowledge_terms)

sp = spacy.load('en_core_web_sm')

class User:
    def __init__(self, name):
        self.name = name
        self.likes = []
        self.dislikes = []

cur_user = User('default')

def mod_likes(word, mode = 'append'):
    global cur_user

    if mode == 'append' and word not in cur_user.likes:
        # remove word from dislikes list
        mod_dislikes(word, mode = 'remove')

        # append word to likes list
        cur_user.likes.append(word)
        return True
    elif mode == 'remove' and word in cur_user.likes:
        # remove word from likes list
        cur_user.likes.remove(word)
        return True
    else:
        # word is already in list
        return False
    
def mod_dislikes(word, mode = 'append'):
    global cur_user

    if mode == 'append' and word not in cur_user.dislikes:
        # remove word from likes list
        mod_likes(word, mode = 'remove')
        
        # append word to dislikes list
        cur_user.dislikes.append(word)
        return True
    elif mode == 'remove' and word in cur_user.dislikes:
        # remove word from dislikes list
        cur_user.dislikes.remove(word)
        return True
    else:
        # word is already in list
        return False

# helper method to reverse lemmatization of a word and return the original word in the dictionary    
def get_lemmatized_index(lemma):
    for term in knowledge_terms:
        if lemmatizer.lemmatize(term) == lemma:
            return term
        

# return subjects of a sentence
def get_subjects(sentence):

    # NEED TO ADD MORE LABELS
    # NEED TO ADD MORE LABELS
    labels = ['lsubj']
    doc = sp(sentence)
    subject_tok = [token.text for token in doc if token.dep_ in labels]

    subject_tok.reverse()
    return subject_tok

# get one subject from list of possible subjects of a sentence
def get_one_subject(sentence):
    # get list of subjects
    tok = get_subjects(sentence)
    # return first subject in list
    lemma = tok[0]
    return lemma

def sentiment_scores(sentence):

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

    # print("Sentence Overall Rated As", end = " ")
    if sentiment_dict['compound'] >= 0.05:
        return("Positive")
    elif sentiment_dict['compound'] <= - 0.05:
        return("Negative")
    else:
        return("Objective")




# --------------------- MAIN ---------------------

# open intents file
with open('intents.json') as json_data:
    intents = json.load(json_data)

# load in training data from the model
data = pickle.load(open('model/training_data.pkl', 'rb'))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# load in model
model = pickle.load(open('model/neural_model.pkl', 'rb'))

# load users


# START CHAT
# start chat by asking for user's name
os.system('clear')
debug = False

if debug:
    get_usrname()

    while not bye:
        user_input = input('You: ')
        print('Bot: ', end = '')
    quit()

# CHATBOT GUI

# create GUI
root = Tk()
root.title('Chatbot')

