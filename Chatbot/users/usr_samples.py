# user model samples to test the chatbot

import pickle

class User:
    def __init__(self, name, likes, dislikes):
        self.name = name
        self.likes = likes
        self.dislikes = dislikes

# user samples
usr1 = User('Vicky', ['starry night', 'sunflowers'], ['asylum'])
usr2 = User('Shu', ['paintings', 'asylum'], ['sunflowers'])

users_data = [usr1, usr2]

pickle.dump(users_data, open("users_data.pkl", "wb"))
