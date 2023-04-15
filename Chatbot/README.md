# How To Run the Chatbot
--
### Note: This project was done using Python 3.10.10

1. Please download and extract the Chatbot zip file

2. In a terminal, please run the following command:

''' 
pip install -r requirements.txt
'''

You might need to also install spaCy dependency:
'''
python -m spacy download en_core_web_sm
'''

There may be other dependencies that are required such as nltk so you may need to use this to help install the correct dependencies.

3. **If you do not wish to modify the chatbot's model or user models, skip to step 5.** Otherwise, create a new model using train_chatbot.py located in the 'model' folder.

4. If you wish to ever reset or modify the starting user models, run usr_samples.py in the 'users' folder.

5. Run chatbot.py