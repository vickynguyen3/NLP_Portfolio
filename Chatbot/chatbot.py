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
import spacy

stopwords = set(stopwords.words('english'))
stopwords = stopwords - set(['no', 'not', 'nor', 'don', 'don\'t', 'ain', 'aren', 'aren\'t', 'couldn', 'couldn\'t', 'didn', 'didn\'t', 'doesn', 'doesn\'t', 'hadn', 'hadn\'t', 'hasn', 'hasn\'t', 'haven', 'haven\'t', 'isn', 'isn\'t', 'mightn', 'mightn\'t', 'mustn', 'mustn\'t', 'needn', 'needn\'t', 'shan', 'shan\'t', 'shouldn', 'shouldn\'t', 'wasn', 'wasn\'t', 'weren', 'weren\'t', 'won', 'won\'t', 'wouldn', 'wouldn\'t'])

usr_name = ''
context = ['']
bye = False
lemmatizer = WordNetLemmatizer()

# dictionary 
# {word: sentences that contain the word}
knowledge_base = pickle.load(open('knowledge_base.p', 'rb'))

# lemmatize words in knowledge base
knowledge_facts = knowledge_base.keys()

# test
print(knowledge_facts)

# NLP for dependency parsing
sp = spacy.load('en_core_web_sm')


# --------------------- USER CONSTRUCTOR ---------------------
class User:
    def __init__(self, name):
        self.name = name
        self.likes = []
        self.dislikes = []

cur_user = User('default')

# --------------------- MODIFY LIKES & DISLIKES METHODS ---------------------

# modify likes
def mod_likes(word, mode = 'append'):
    global cur_user

    if mode == 'append' and word not in cur_user.likes:
        # remove word from dislikes list
        mod_dislikes(word, mode = 'remove')

        # append word to likes list
        cur_user.likes.append(word)
        
        return True
    
    if mode == 'remove' and word in cur_user.likes:
        # remove word from likes list
        cur_user.likes.remove(word)
        
        return True
    
    return False

# modify dislikes
def mod_dislikes(word, mode = 'append'):
    global cur_user

    if mode == 'append' and word not in cur_user.dislikes:
        # remove word from likes list
        mod_likes(word, mode = 'remove')
        
        # append word to dislikes list
        cur_user.dislikes.append(word)

        return True
    
    if mode == 'remove' and word in cur_user.dislikes:
        # remove word from dislikes list
        cur_user.dislikes.remove(word)

        return True
    
    return False

# --------------------- SENTIMENT ANALYSIS METHODS ---------------------

# use vader sentiment analysis to determine if a sentence is positive, negative, or objective
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05:
        return("Positive")
    elif sentiment_dict['compound'] <= - 0.05:
        return("Negative")
    else:
        return("Objective")
    
# ---------------------  SUBJECTS & CONTEXT METHODS ---------------------

# helper method to reverse lemmatization of a word and find the corresponding key in dictionary
def get_lemmatized_index(lemma):
    for key in knowledge_facts:
        if lemmatizer.lemmatize(key) == lemma:
            return key
        

# return subjects of a sentence
def get_subjects(sentence):
    labels = ['nsubj', 'nsubjpass', 'csubj', 'csubjpass', 'pobj', 'dobj', 'acomp']
    # spacy dependency parsing
    doc = sp(sentence)

    subject_tok = [token.text for token in doc if token.dep_ in labels]
    
    # test
    print('subject tokens: ', subject_tok)

    subject_tok.reverse()

    # test
    print('reversed subject tokens: ', subject_tok)
    
    return subject_tok

# get one subject from list of possible subjects of a sentence
def get_one_subject(sentence):
    # get list of subjects
    tok = get_subjects(sentence)

    # return first subject in list
    lemma = tok[0]

    return lemma


def match_subjects(sentence):
    global knowledge_facts

    toks = get_subjects(sentence)

    lemma_facts = [lemmatizer.lemmatize(fact) for fact in knowledge_facts]
    print(lemma_facts)

    # lemmatize subjects and compare word to the knowledge base
    for subj in toks:
        lemma_subject = lemmatizer.lemmatize(subj)
        
        print('lemma subject: ', lemma_subject)
        
        # check if sentence contains a subject that is in knowledge base
        if lemma_subject in lemma_facts:
            # return a random sentence from knowledge base
            return random.choice(knowledge_base[get_lemmatized_index(lemma_subject)])

    # no matches found, default to standard response
    return None

def match_context(lst):
    global context
   
    # check if user has at least one qualifying contexts for intent
    for cntxt in lst:
        if cntxt in context:
            return True
    
    return False

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
    bag = [0] * len(words)

    # mark which words are in the sentence
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1

    return np.array(bag)

# predict the intent using a bag of words, returns descending list of probable responses
def classify(sentence):
    print(f'sentence: {sentence}')
    ERR_MARGIN = 0.25

    # generate probabilities from the model
    model_results = model.predict([bag_of_words(sentence, words)])[0]
    # filter out predictions below a threshold/margin
    model_results = [[i, r] for i, r in enumerate(model_results) if r > ERR_MARGIN]

    # sort by strength of probability and reverse it to descending order so most probable is first
    model_results.sort(key = lambda x: x[1], reverse = True)
    
    return_list = []

    for r in model_results:
        return_list.append((classes[r[0]], r[1]))
    print(f'return list: {return_list}')

    return return_list

# --------------------- USER RESPONSE ---------------------

def view_user_dict(datalist):

    for user in datalist:
        print(f'User: {user.name}')
        print(f'Likes: {user.likes}')
        print(f'Dislikes: {user.dislikes}')



def response(sentence):
    global context
    global bye
    global cur_user
    global users_data

    # test
    print(f'cur context: {context}')

    # get response results
    response_results = classify(sentence)

    # test
    print(f'response results: {response_results}')
    
    if response_results:

        while response_results:

            for i in intents['intents']:

                # find a tag matching the first result
                if i['tag'] == response_results[0][0]:

                    # test
                    print(f'len(get_subjects: {len(get_subjects(sentence))}')
                    print(f'match_subjects: {match_subjects(sentence)}')

                    # check for strong sentiments of words in knowledge base before using knowledge base and intents
                    if sentiment_scores(sentence) == 'Positive' and len(get_subjects(sentence)) > 0 and match_subjects(sentence) != None:
                        # test
                        print('positive')

                        lemma = get_one_subject(sentence)
                        mod_likes(lemma, mode = 'append')
                        
                        print(f'current user likes: {cur_user.likes}')

                        return 'I\'m happy to hear that! I\'ll keep that in mind!'
                
                    elif sentiment_scores(sentence) == 'Negative' and len(get_subjects(sentence)) > 0 and match_subjects(sentence) != None:
                        # test
                        print('negative')

                        lemma = get_one_subject(sentence)
                        mod_dislikes(lemma, mode = 'append')
                        
                        print(f'current user dislikes: {cur_user.dislikes}')

                        return 'I\'m sorry to hear that. I\'ll keep that in mind!'
                    
                    else:
                        subject_match = match_subjects(sentence)

                        # check if we can answer with knowledge base
                        if subject_match != None:
                            # test
                            print(i['tag'])
                            # print random response that's related to subject
                            return subject_match
                        
                        # test
                        print('intent', i)
                        print('context req: ', i['context_req'])

                        # if no matching subjects or strong sentiments, use default intents
                        if match_context(i['context_req']) or i['context_req'] == [""]:
                            # test
                            print('cur tag: ', i['tag'])

                            # set new context
                            context = i['context_set']
                            
                            # test
                            print(f'new context: {context}')

                            # get a random response from the intent
                            random_response = random.choice(i['responses'])

                            if i['tag'] == 'dislikes':
                                # retrieve random fact from user's dislikes
                                fact = random.choice(cur_user.dislikes)
                                # concatenate fact to response
                                random_response = random_response + fact

                            if i['tag'] == 'likes':
                                # retrieve random fact from user's likes
                                fact = random.choice(cur_user.likes)
                                # concatenate fact to response
                                random_response = random_response + fact

                            # if user wants to exit
                            if i['tag'] == 'bye':
                                bye = True

                                # save user data before exiting
                                view_user_dict(users_data)
                                pickle.dump(users_data, open('users/users_data.pkl', 'wb'))

                            # a random response for intent
                            return random_response
            # no context match for cur intent, go to the next one
            response_results.pop(0)
        
        # there are matching intents but no matching context
        for i in intents['intents']:
            if i['tag'] == 'noanswer' or i['tag'] == 'teach':
                return random.choice(i['responses'])
    # no matching intents within the error margin
    else:
        return 'I\'m sorry, I don\'t understand.'

def ask_name():
    return 'Hello! What is your name?'

def greet_usr():
    # get greeting intent
    for i in intents['intents']:
        if i['tag'] == 'greeting':
            # get a random response from the intent
            return random.choice(i['responses'])

def welcome_back():
    # get welcome back intent
    for i in intents['intents']:
        if i['tag'] == 'welcome_back':
            # get a random response from the intent
            return random.choice(i['responses'])
    
def exit():
    global bye
    return bye

# start the conversation before main loop
def get_usrname(usr_name):
    global cur_user
    global users_data

    print(ask_name())

    # test
    #usr_name = input('>>').lower()

    returning_usr = False
    
    # check if it's a returning user
    for usr in users_data:
        if usr_name.lower() == usr.name.lower():
            # set current user based on user data
            cur_user = usr

            
            # test
            print('cur user: ', cur_user)
            print(welcome_back())

            returning_usr = True
            break
    
    # if it's a new user
    if not returning_usr:
        # create new user
        cur_user = User(usr_name)
        users_data.append(cur_user)

        # test 
        print(' new cur user: ', cur_user.name)
        print(greet_usr())

        return greet_usr()
    
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
users_data = pickle.load(open('users/users_data.pkl', 'rb'))

# START CHAT
# start chat by asking for user's name
os.system('clear')
debug = False

if debug:
    get_usrname('test')

    while not bye:
        user_input = input('>>')
        print(response(user_input))
    quit()

# CHATBOT GUI

root = Tk()
root.title('Chatbot')

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

first_time = True

def send():
    global first_time

    if first_time:
        send = '>>' + e.get()
        txt.insert(END, '\n' + send)
        txt.insert(END, '\n' + get_usrname(e.get()))
        e.delete(0, END)
        first_time = False
    else:
        send = '>>' + e.get()
        txt.insert(END, '\n' + send)
        txt.insert(END, '\n' + response(e.get()))
        e.delete(0, END)

    # check for exit flag
    if exit():
        root.quit()

# GUI layout
lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Van Gogh Bot", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(txt)
scrollbar.place(in_=txt, relheight=1, relx=1.0, bordermode='outside')

e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)


# main conversation loop
txt.insert(END, '\n' + ask_name())
root.mainloop()
