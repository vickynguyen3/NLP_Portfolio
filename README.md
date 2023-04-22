# NLP_Portfolio
This is a NLP Portfolio for CS 4395

---
## Overview of NLP
This is a [document](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/OverviewOfNLP.pdf) describing an overview of Natural Language Processing.

---
## Homework 1: Text Processing with Python
The program processes the text of a file and corrects the format of the employee list. The user will need to input the correct format when
the program has found an error. After the progam has finished correcting the format, it will output the employee list to show: employee ID, first name, middle name, last name, and phone #

### How to run the program:
py Homework1_vtn180004.py data/data.csv

### Strength and Weakness
The strength of python is that
it is very high level and makes it easier to search such as the keys() or re.search(). The weakness of Python in my opinion is that there's no declaration for variables so I find it difficult to keep track or hard to find the error. For example, I had an error in my code, but I wasn't sure what the error is coming from and realized it came from my variable not being the same as what I typed in the parameter.

### What I've Learned 
I learned how to utilize several variations of python functions such as
input(), capititalize, keys(), search(), etc. I learned how to use
dictionary and pickle.

[Code is here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Homework1/Homework1_vtn180004.py)

---
## Word Guessing Game
A program using Python and NLTK features to explore a text file and create a word guessing game. The program first extracts text from a large file that is from a chapter of an anatomy textbook. Then, we would do a preprocessing of the text and calculate the lexical diversity of the tokenized text. Afterwards, we would make a dictionary and output the top 50 most common words and use it for our word guessing game. 

You can find the [code here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/WordGuessingGame/WordGuess_vtn180004.py) and the [anatomy text here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/WordGuessingGame/anat.txt)

---
## WordNet Exploration
I created a Python notebook documenting my experience using WordNet and SentiWordNet from NLTK. I also learned how to identify collocations.

You can find the [notebook here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/WordNet-vtn180004.ipynb)

---
## Sentence Parsing
Drawings to understand the concepts related to sentence syntax as well as understand and utilize the 3 types of sentences parses: PSG, dependency, and SRL. 

You can find the [paper here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/parsingsentences-vtn180004.pdf)

---
## N-Gram Language Model
Building a language model from ngrams and a reflection on the utility of ngram language models. You can find the [Narrative](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/N-grams/N-GramsNarrative.pdf) here.

We created a bigram and unigram dictionaries for English, French, and Italian using the provided training data where the key is the unigram or bigram text. The value is the count of that unigram and bigram in the data. You can find [Program 1](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/N-grams/main.py) here. We also outputted our program's [predictions](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/N-grams/predictions.txt) for each line of text into a file found here.

We then calculate the probabilities for each langauge and compare against the true labels. You can find [Program 2](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/N-grams/calculate.py) here.

---
## Web Crawler

Creating a simple web crawler [program](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/WebCrawler/webcrawler.py) that starts off with a given URL, and scrapes the texts from other URLs on that page. We chose our starter URL to be a wikipedia of Hayao Miyazaki, and chose the topic to be about anime.

We analyzed our scrape data by using TF-IDF to find the most important terms relating to our topic in our [program](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/WebCrawler/importantterms.py). The program then pickles the [facts](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/WebCrawler/facts.txt) to a dictionary and text file, which can be found here.

[Read Me - Web Crawler](https://github.com/meintgl/NLP-Portfolio/blob/main/Webcrawler_mdc190005/readme.md)

--
## SKLearn and Text Classification

[Python notebook](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Sklearn/textclass-vtn180004.ipynb) that documents my experiences using text classification by using a data set from Kaggle that involved tweets related to COVID-19 and made attempts to use ML algorithms such as Naive Bayes, Logistics Regression, and Neural Networks.

--
## ACL Paper Summary
It a summary of the ACL Paper, “Perceiving the World: Question-guided Reinforcement Learning for Text-based Games”. You can find it [here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/CS4395.001ACL.pdf)

--
## Chatbot
Created [basic chatbot](https://github.com/vickynguyen3/NLP_Portfolio/tree/main/Chatbot) using NLP techniques learned in class. The Chatbot can carry on a limited conversation on topics about Vincent Van Gogh. You can find the report [here](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/ChatbotReport-vtn180004.pdf)

### How To Run the Chatbot

**Note: This project was done using Python 3.10.10**

**STEP 1:** Please download and extract the [Chatbot zip file](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot.zip)

**STEP 2:** In a terminal, please run the following command:

``` 
pip install -r requirements.txt 
```

You might need to also install spaCy dependency:
```
python -m spacy download en_core_web_sm
```

There may be other dependencies that are required such as nltk so you may need to use [this](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/nltk_dependency.py) to help install the correct dependencies.

**STEP 3: If you do not wish to modify the chatbot's model or user models, skip to STEP 5.** Otherwise, you may create a new model using [train_chatbot.py](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/model/train_chatbot.py), which is located in the 'model' folder.

**STEP 4:** If you want to reset or modify the starting user models, run [usr_samples.py](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/users/usr_samples.py), which is located in the 'users' folder.

**STEP 5:** Run [chatbot.py](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/chatbot.py)

--
## Text Classification 2
Gaining experience with Keras, text classification, and deep learning model variations and embeddings. I used a Kaggle data sets, which is about the sentiments related to COVID-19 and the pandemic, and attempted to predict their sentiments using different architecture such as RNN. The code and comments can be found in the [notebook](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Sklearn/txtclassification2-vtn180004.ipynb).
