import random

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from . import config, utils

class Player:

    def __init__(self, name, color='#FFFFFF'):
        self.account = config.START_ACCOUNT
        self.hand = []
        self.name = name
        self.color = color
        self.active = True

    def new_distribution(self):
        self.hand = []
        self.active = True

    def bet(self, data):
        player_bet = random.choice([1, 1, 2, 3, 4, 5])
        return player_bet

    def hand_value(self, table):
        hand = [Card(*card) for card in utils.card_values(self.hand)]
        table = [Card(*card) for card in utils.card_values(table)]
        score = HandEvaluator.evaluate_hand(hand, table)
        return score

players = [Player(str(player)) for player in range(1,5)]
