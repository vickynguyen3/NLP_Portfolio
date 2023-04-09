# Vicky Nguyen, vtn180004
# CS 4395.001
# Chatbot Project - Model Training

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow as tf

# impout our chatbot intents file
import json
with open('../intents.json') as json_data:
    intents = json.load(json_data)