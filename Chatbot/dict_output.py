import pickle

dict = pickle.load(open('knowledge_base.p', 'rb'))

with open("dictionary_output.txt", "a") as f:
    for key in dict.keys():
        print('Facts About: ', key, file = f)
        print(dict[key], file = f)
        print('-----------------', file = f)


    
