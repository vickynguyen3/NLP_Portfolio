# Vicky Nguyen, vtn180004
# Meinhard Capucao, mdc190005
# CS 4395.001

from bs4 import BeautifulSoup
import requests
import re
from nltk.tokenize import sent_tokenize

# helper function to determine if an element is visible 
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

# function to loop thru URLs and scrape all text off each page
def scrapeTxt(url_list):   
    # loop thru URLs scrape all text off the page
    for i, url in enumerate(url_list):
        # open url
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        data = soup.findAll(text=True)
        # filter to make sure its only visible data
        result = filter(visible, data)
        # list from filter
        temp_list = list(result)      
        temp_str = ' '.join(temp_list)
    
        # ----- clean text -----        
        # delete newlines and tabs first
        clean_list = temp_str.split()
        clean_list = [token for token in clean_list if token.isascii()]
        clean_str = ' '.join(clean_list)

        # extract sentences w/ NLTK's sentence tokenizer
        sentences = sent_tokenize(clean_str)

        url_name = 'data/url_text' + str(i) + '.txt'
        # store each page's text in its own file
        with open(url_name, 'w') as f:
            for sent in sentences:
                #print(sent)
                # write sentences for each file to a new file
                f.write(sent + '\n')

    return

# --------- main ---------
# Topic - anime

# starts with a URL representing topic
starter_url = "https://en.wikipedia.org/wiki/Hayao_Miyazaki"

r = requests.get(starter_url)
data = r.text
soup = BeautifulSoup(data)
counter = 0
url_list = []

# loop thru text to find all hyperlinks
for link in soup.find_all('a'):
    # at least 15 relevant URLs
    if counter > 20:
        break
    
    link_str = str(link.get('href'))
    #print(link_str)

    # filter URLs using target keywords and/or ignoring useless URLs
    #if 'hayao' in link_str.lower() or 'miyazaki' in link_str.lower() or 'hayao-miyazaki'in link_str.lower() or 'hayao_miyazaki' in link_str.lower():
    if 'anime' in link_str.lower():
        if link_str.startswith('/url?q='):
            # remove /url?q=
            link_str = link_str[7:]
            # output modified url
            print('MOD:', link_str)

        if '&' in link_str:
            i = link_str.find('&')
            # remove & and everthing after &
            link_str = link_str[:i]

        # link starts with http and is not from google
        if link_str.startswith('http') and 'google' not in link_str and 'wikipedia' not in link_str and 'wikimedia' not in link_str and 'animekon' not in link_str and 'wsj' not in link_str:
            print(str(counter) + ': ' + link_str)
            # append url to the list
            url_list.append(link_str)
            counter += 1

print('Finished printing list of URLs...')

# call function to loop thru URLs and scrape all text off each page
scrapeTxt(url_list)