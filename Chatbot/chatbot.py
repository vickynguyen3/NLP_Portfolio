# Vicky Nguyen, vtn180004
# CS 4395.001
# Chatbot Project

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import random
import json
import pickle
import sklearn
from sklearn.neural_network import MLPClassifier
import os
from tkinter import *

stopwords = set(stopwords.words('english'))
stopwords = stopwords - set(['no', 'not', 'nor', 'don', 'don\'t', 'ain', 'aren', 'aren\'t', 'couldn', 'couldn\'t', 'didn', 'didn\'t', 'doesn', 'doesn\'t', 'hadn', 'hadn\'t', 'hasn', 'hasn\'t', 'haven', 'haven\'t', 'isn', 'isn\'t', 'mightn', 'mightn\'t', 'mustn', 'mustn\'t', 'needn', 'needn\'t', 'shan', 'shan\'t', 'shouldn', 'shouldn\'t', 'wasn', 'wasn\'t', 'weren', 'weren\'t', 'won', 'won\'t', 'wouldn', 'wouldn\'t'])

usr_name = ''
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
    
def match_subjects(sentence):
    global knowledge_terms

    toks = get_subjects(sentence)

    terms_lemma = [lemmatizer.lemmatize(term) for term in knowledge_terms]
    print(terms_lemma)

    # lemmatize subjects and check if they are in the knowledge base
    for subject in toks:
        subject_lemma = lemmatizer.lemmatize(subject)
        
        print('subject lemma: ', subject_lemma)
        
        if subject_lemma in terms_lemma:
            # return a random sentence from the knowledge base
            return random.choice(knowledge_base[get_lemmatized_index(subject_lemma)])

    # no matches found, default to standard response
    return None

def match_context(lst):
    global context
    # check if any of the contexts in the list are in the current context
    for cntxt in lst:
        # if context is in the list of contexts
        if cntxt in context:
            return True
    return False

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)

    # stem each word - create short form for word
    stemmer = LancasterStemmer
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words if word.isalpha() and word not in stopwords]
    
    return sentence_words

def bag_of_words(sentence, words):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)

    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1

    return np.array(bag)

def classify(sentence):

    err_margin = 0.25

    # generate probabilities from the model
    model_results = model.predict([bag_of_words(sentence, words)])[0]
    # filter out predictions below a threshold
    model_results = [[i, r] for i, r in enumerate(model_results) if r > err_margin]

    # sort by strength of probability
    model_results.sort(key = lambda x: x[1], reverse = True)
    return_list = []

    for r in model_results:
        return_list.append((classes[r[0]], r[1]))
    print(f'return list: {return_list}')
    # return tuple of intent and probability
    return return_list

# --------------------- USER RESPONSE ---------------------

def response(sentence):
    global context
    global bye
    global cur_user

    print(f'cur context: {context}')

    # generate probabilities from the model
    response_results = classify(sentence)
    print(f'response results: {response_results}')
    
    if response_results:
        # loop as long as there are matches to process
        while response_results:

            for i in intents['intents']:

                # find a tag matching the first result
                if i['tag'] == response_results[0][0]:

                    print(f'len(get_subjects: {len(get_subjects(sentence))}')
                    print(f'match_subjects: {match_subjects(sentence)}')

                    # check for strong sentiments of words in knowledge base before using knowledge base and intents
                    if sentiment_scores(sentence) == 'Negative' and len(get_subjects(sentence)) > 0 and match_subjects(sentence) != None:
                        print('negative')

                        lemma = get_one_subject(sentence)
                        mod_dislikes(lemma, mode = 'append')
                        return 'I\'m sorry to hear that. I\'ll keep that in mind!'
                    elif sentiment_scores(sentence) == 'Positive' and len(get_subjects(sentence)) > 0 and match_subjects(sentence) != None:
                        print('positive')

                        lemma = get_one_subject(sentence)
                        mod_likes(lemma, mode = 'append')
                        return 'I\'m glad to hear that. I\'ll keep that in mind!'
                    else:
                        subject_match = match_subjects(sentence)

                        if subject_match != None:
                            return subject_match
                        
                        print('intent', i)
                        print('context req', i['context_req'])

                        if match_context(i['context_req']) or i['context_req'] == [""]:
                            print('cur tag: ', i['tag'])

                            context = i['context_set']
                            print(f'new context: {context}')

                            random_response = random.choice(i['responses'])

                            if i['tag'] == 'dislikes':
                                term = random.choice(cur_user.dislikes)
                                random_response = random_response + term

                            if i['tag'] == 'likes':
                                term = random.choice(cur_user.likes)
                                random_response = random_response + term

                            if i['tag'] == 'bye':
                                bye = True
                                pickle.dump(users_data, open('users_data.pkl', 'wb'))

                            # a random response from the intent
                            return random_response
            
            response_results.pop(0)
        
        for i in intents['intents']:
            if i['tag'] == 'noanswer':
                return random.choice(i['responses'])
    else:
        return 'I\'m sorry, I don\'t understand.'

def ask_name():
    return 'Hello! What is your name?'

def greet_back(name):
    return 'I am Van Gogh Bot, ' + name + '! How can I help you?'

def greet_usr():
    # get greeting intent
    for i in intents['intents']:
        if i['tag'] == 'greeting':
            return random.choice(i['responses'])

def welcome_back():
    # get welcome back intent
    for i in intents['intents']:
        if i['tag'] == 'welcome_back':
            return random.choice(i['responses'])
    
def exit():
    global bye
    return bye

# start the conversation before main loop
def get_usrname(usr_name):
    global cur_user
    global users_data

    print(ask_name())
    usr_name = input('You: ').lower()

    returning_usr = False
    
    for usr in users_data:
        if usr_name == usr.name.lower():
            cur_user = usr
            returning_usr = True
            break
    
    if not returning_usr:
        cur_user = User(usr_name)
        users_data.append(usr)
        return greet_back(usr_name)
    
    return welcome_back()
    


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

