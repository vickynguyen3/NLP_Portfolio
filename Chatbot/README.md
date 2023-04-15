# How To Run the Chatbot

**Note: This project was done using Python 3.10.10**


**STEP 1:** Please download and extract the [Chatbot zip file]()

**STEP 2:** In a terminal, please run the following command:

 
``` 
pip install -r requirements.txt 
```


You might need to also install spaCy dependency:
```
python -m spacy download en_core_web_sm
```

There may be other dependencies that are required such as nltk so you may need to use [this](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/nltk_dependency.py) to help install the correct dependencies.

**STEP 3: If you do not wish to modify the chatbot's model or user models, skip to STEP 5.** Otherwise, you may create a new model using [train_chatbot.py](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/model/train_chatbot.py) located in the 'model' folder.

**STEP 4:** If you want to reset or modify the starting user models, run [usr_samples.py](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/users/usr_samples.py) in the 'users' folder.

**STEP 5:** Run [chatbot.py](https://github.com/vickynguyen3/NLP_Portfolio/blob/main/Chatbot/chatbot.py)