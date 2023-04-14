import pickle

class User:
    def __init__(self, name):
        self.name = name
        self.likes = []
        self.dislikes = []

usrs_info = pickle.load(open("usrs_info.p", "rb"))

for usr in usrs_info:
    print('User Name: ', usr.name)
    print('Likes: ', usr.likes)
    print('Dislikes: ', usr.dislikes)
    print('------------------------')
