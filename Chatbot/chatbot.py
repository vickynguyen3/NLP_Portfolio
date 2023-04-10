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


