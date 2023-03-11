import math
import nltk
import requests
import pickle
import re
import spacy
import random
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

stopwords = stopwords.words('english')  # Prints constant stopwords

docs = {}
# Creates a dictionary that contains the doc_url_text{i} as the key, and the actual text as the value. Does it 21
# times which represents all URL calls.
for i in range(21):
    filename = f"data/url_text{i}.txt"
    with open(filename, 'r') as f:
        doc_text = f.read()
        # Remove occurrences of months
        doc_text = doc_text.replace('January', ' ')
        doc_text = doc_text.replace('February', ' ')
        doc_text = doc_text.replace('March', ' ')
        doc_text = doc_text.replace('August', ' ')
        doc_text = doc_text.replace('June', ' ')
        doc_text = doc_text.replace('November', ' ')
        doc_text = doc_text.replace('December', ' ')
        doc_text = doc_text.replace('September', ' ')
        doc_text = doc_text.replace('July', ' ')
        # Remove occurrences of 'yet'
        doc_text = doc_text.replace('yet', '')
        docs[f"doc_url_text{i}"] = doc_text

# function to process facts, removing symbols
def cleanup_facts(text):
    # Remove brackets characters and single quotation tabs
    text = re.sub(r'[\[\]\']', '', text)
    return text


# function to create tf dictionaries (from prof. mazidi online code)
def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc)
    tokens = [w for w in tokens if w.isalpha() and w not in stopwords]

    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
    return tf_dict


# creates a tdf-idf dict for each document (from prof. mazidi online code)
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf

# function to print a random fact from a random term
def get_random_fact():
    term = random.choice(list(clean_term_dicts.keys()))
    fact = random.choice(clean_term_dicts[term])
    return f"{term}: {fact}"

# function to print a random fact from a specific term
def get_fact_for_term(term):
    if term in clean_term_dicts:
        fact = random.choice(clean_term_dicts[term])
        return f"Here's a random act about {term}: \n {fact}"
    else:
        return f"No facts for: {term}"

# function to get all facts from a specified term
def get_all_facts_about_term(term: str):
    if term not in clean_term_dicts:
        print(f"No facts for '{term}'")
        return
    print(f"All facts about '{term}':")
    for fact in clean_term_dicts[term]:
        print(f"\t- {fact}")

# Function to get all facts
def get_all_facts():
    for term, facts in clean_term_dicts.items():
        print(f"{term}:")
        for fact in facts:
            print(f"\t- {fact}")

# Function to print all facts into a text file called facts.txt
def write_all_facts():
    with open("facts.txt", "w") as f:
        for term, facts in clean_term_dicts.items():
            f.write(f"{term}:\n")
            for fact in facts:
                f.write(f"- {fact}\n")

# create a dictionary to store TF dictionaries for each document
tf_docs = {}

# iterate over each document
for doc_name, doc_text in docs.items():
    # create a TF dictionary for the document
    tf_doc = create_tf_dict(doc_text)
    # print(f"TF dictionary for {doc_name}: {tf_doc}")
    # add the TF dictionary to the dictionary of TF dictionaries,
    # using the document name as the key
    tf_docs[doc_name] = tf_doc

# creates a set of vocabs to find the number of unique words
vocab_sets = []
for doc_name, tf_doc in tf_docs.items():
    vocab_sets.append(set(tf_doc.keys()))
vocab = set().union(*vocab_sets)
print("number of unique words:", len(vocab))

# sets vocal by topic
vocab_by_topic = [set(tf_docs[doc_name].keys()) for doc_name in tf_docs]

idf_dict = {}

# sets numdocs to total url texts, then finds idf for each one
num_docs = len(tf_docs)
for term in vocab:
    temp = ['x' for voc in vocab_by_topic if term in voc]
    idf_dict[term] = math.log((1 + num_docs) / (1 + len(temp)))

# create a dictionary to store the TF-IDF dictionaries
tfidf_docs = {}

# loop through each document and create its TF-IDF dictionary
for doc_name, tf_doc in tf_docs.items():
    tfidf_doc = create_tfidf(tf_doc, idf_dict)
    # add the TF-IDF dictionary to the dictionary of TF-IDF dictionaries,
    # using the document name as the key
    tfidf_docs[doc_name] = tfidf_doc

# make list of anime terms, and non anime terms
anime_terms = []
non_anime_terms = []
for doc_name, tfidf_doc in tfidf_docs.items():
    # find the highest tf-idf terms for this document
    doc_term_weights = sorted(tfidf_doc.items(), key=lambda x: x[1], reverse=True)

    # print the top 20 highest weighted terms for this document
    # print(f"\n{doc_name}: ", [term for term, weight in doc_term_weights[:20]])

    # adds the next 10 anime terms (with capital letters. would use spacy but not currently working on setup :( )
    # ideally would use spacy for proper nouns to find anime titles, something to implement
    anime_terms.extend(
        [term for term, weight in doc_term_weights[:10] if term not in anime_terms and term[0].isupper()])

    # adds next 6 non anime terms (lowercase start) if it is not already there
    non_anime_terms.extend([term for term, weight in doc_term_weights[:6]
                            if term not in non_anime_terms and term[0].islower()])


# Remove some terms that don't make sense, or arent as important
non_anime_terms.remove("comments")
non_anime_terms.remove("says")
non_anime_terms.remove("wants")
non_anime_terms.remove("views")
non_anime_terms.remove("session")
non_anime_terms.remove("stated")
non_anime_terms.remove("index")
non_anime_terms.remove("store")
non_anime_terms.remove("women")

print("10 important term words that aren't anime titles, according to tdf-idf: ", non_anime_terms)

fact_dict = {}  # Create a dictionary of facts

for i in range(21):
    filename = f"data/url_text{i}.txt"
    with open(filename, "r") as f:
        text = f.read()
        text = text.replace('\n', ' ')
    # split the text into sentences
    sentences = text.split(". ")
    # loop over each sentence and check if it contains any of the terms

fact_dict = {}  # Create a dictionary of facts
counter = 1

# Loops through all 21 docs to create sentences with each term. Cleanup can and will be done later on
for i in range(21):
    filename = f"data/url_text{i}.txt"
    with open(filename, "r") as f:
        text = f.read()
        # makes sure all new lines are gone, just in case.
        text = text.replace('\n', ' ')
    # split the text into sentences
    sentences = text.split(". ")
    # loops over each sentence and checks if it contains terms. if it does, append it to fact dict
    for sentence in sentences:
        for term in non_anime_terms:
            if term in sentence.lower():
                # if the sentence already has the term, add it to dictionary
                if term in fact_dict:
                    fact_dict[term].append(f"Fact {counter}: {sentence}")
                # if not, create a new term
                else:
                    fact_dict[term] = [f"Fact {counter}: {sentence}. "]
                counter += 1

# Cleans up all facts by removing some symbols and single quotations from clean_term_dicts function
clean_term_dicts = {}
for term in fact_dict:
    clean_term_dicts[term] = [cleanup_facts(fact) for fact in fact_dict[term]]

# Testing fact functions

# sample code for get_random_fact
# random_fact = get_random_fact()
# print(random_fact)

# sample code for get_fact_for_term
# random_fact = get_fact_for_term("love")
# print(random_fact)

# sample driver code for print_all_facts
# get_all_facts()

# sample driver code for get_all_facts_about_term
#get_all_facts_about_term("love")

#Anime terms is to be implemented later. This currenty has facts for non-anime terms.
filename = "clean_term_dicts.pickle"

with open(filename, "wb") as f:
    # pickle the object to the file
    pickle.dump(clean_term_dicts, f)

write_all_facts()