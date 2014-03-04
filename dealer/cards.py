import random
import itertools

values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
colors = ['C', 'D', 'H', 'S']

class Cards:

    def __init__(self):
        self.deck = [i for i in itertools.product(colors, values)]
        random.shuffle(self.deck)
